"""
monitor.scanner
===============

Модуль для поиска узкой консолидации на последней свече.

Назначение:
    Загружает исторические данные через yfinance, рассчитывает ширину
    ценового коридора и определяет, находится ли инструмент в состоянии
    узкой консолидации.

    Модуль не выводит информацию в консоль и не строит графики.
    Он предназначен исключительно для использования монитором.

Использование:
    >>> from monitor.scanner import is_consolidating_now
    >>> is_consolidating_now("AAPL")
    True
"""

from __future__ import annotations

from typing import Iterable

import pandas as pd
import yfinance as yf

from config import CONSOLIDATION_QUANTILE, WINDOW_5M


def _download_5m_data(ticker: str) -> pd.DataFrame:
    """
    Загружает 5-минутные данные по акции за последние 5 торговых дней.

    Args:
        ticker:
            Биржевой тикер.

    Returns:
        DataFrame с OHLC-данными.

    Raises:
        ValueError:
            Если данные отсутствуют.
    """

    df = yf.download(
        tickers=ticker,
        period="5d",
        interval="5m",
        auto_adjust=True,
        progress=False,
    )
    
    # print(f"{ticker}: {len(df)} candles")
    
    # Проверяем, что данные были загружены
    if df.empty:
        raise ValueError(f"No market data received for '{ticker}'.")

    # yfinance иногда возвращает MultiIndex.
    df.columns = [
        column[0] if isinstance(column, tuple) else column
        for column in df.columns
    ]

    # Удаляем строки с отсутствующими данными
    df = df.dropna(subset=["Open", "High", "Low", "Close"])

    if df.empty:
        raise ValueError(f"No valid OHLC data for '{ticker}'.")

    return df


def _calculate_corridor_width(
    df: pd.DataFrame,
    window: int,
) -> pd.DataFrame:
    """
    Рассчитывает ширину ценового коридора.

    Args:
        df:
            Исторические данные.

        window:
            Размер скользящего окна.

    Returns:
        DataFrame с добавленным столбцом Corridor_Width_%.
    """

    df = df.copy()

    df["Rolling_Max"] = df["High"].rolling(window).max()
    df["Rolling_Min"] = df["Low"].rolling(window).min()

    df["Corridor_Width_%"] = (
        (df["Rolling_Max"] - df["Rolling_Min"])
        / df["Rolling_Min"]
        * 100
    )

    return df


def is_consolidating_now(
    ticker: str,
    window: int = WINDOW_5M,
    quantile: float = CONSOLIDATION_QUANTILE,
) -> bool:
    """
    Проверяет, находится ли акция в узкой консолидации
    на последней свече.

    Args:
        ticker:
            Биржевой тикер.

        window:
            Размер окна расчета.

        quantile:
            Квантиль, определяющий узкий диапазон.

    Returns:
        True, если последняя свеча находится в консолидации,
        иначе False.
    """

    df = _download_5m_data(ticker)
    df = _calculate_corridor_width(df, window)

    threshold = df["Corridor_Width_%"].quantile(quantile)

    last_width = df["Corridor_Width_%"].iloc[-1]

#     print(
#         f"{ticker}: "
#         f"width={last_width:.2f}% | "
#         f"threshold={threshold:.2f}% | "
#         f"consolidating={last_width < threshold}"
# )

    return bool(last_width < threshold)


def scan_watchlist(
    watchlist: Iterable[str],
) -> list[str]:
    """
    Проверяет список тикеров и возвращает акции,
    находящиеся в консолидации.

    Args:
        watchlist:
            Последовательность тикеров.

    Returns:
        Список тикеров, находящихся в консолидации.
    """

    consolidating: list[str] = []

    for ticker in watchlist:
        print(f"Scanning {ticker}...")
        
        try:
            if is_consolidating_now(ticker):
                consolidating.append(ticker)
        except Exception as error:
            # Ошибка одного тикера не должна останавливать монитор.
            print(f'[ERROR] {ticker}: {error}')
            continue

    return consolidating
    # return ['CRDO', 'RKBL']