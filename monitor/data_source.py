"""
monitor.data_source
===================

Модуль для получения исторических рыночных данных.

Назначение:
    Предоставляет единый интерфейс для загрузки исторических данных
    из различных источников.

    На текущем этапе поддерживаются:
        - Yahoo Finance (через yfinance);
        - локальные файлы Parquet.

    В дальнейшем модуль может быть расширен поддержкой:
        - Polygon.io;
        - Interactive Brokers (IBKR);
        - CSV;
        - других поставщиков данных.

Использование:
    >>> from monitor.data_source import download_from_yahoo
    >>> df = download_from_yahoo("AAPL")

    >>> from monitor.data_source import load_parquet
    >>> df = load_parquet("AAPL")
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf

from config import MARKET_DATA_DIR


def download_from_yahoo(
    ticker: str,
    period: str = "5d",
    interval: str = "5m",
) -> pd.DataFrame:
    """
    Загружает исторические данные из Yahoo Finance.

    Args:
        ticker:
            Биржевой тикер.

        period:
            Период загрузки.

        interval:
            Таймфрейм.

    Returns:
        DataFrame с историческими OHLCV-данными.

    Raises:
        ValueError:
            Если данные отсутствуют.
    """

    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
    )

    if df.empty:
        raise ValueError(
            f"No market data received for '{ticker}'."
        )

    # yfinance иногда возвращает MultiIndex.
    df.columns = [
        column[0] if isinstance(column, tuple) else column
        for column in df.columns
    ]

    df = df.dropna(
        subset=["Open", "High", "Low", "Close"]
    )

    if df.empty:
        raise ValueError(
            f"No valid OHLC data for '{ticker}'."
        )

    return df


def load_parquet(
    ticker: str,
    interval: str = "5m",
) -> pd.DataFrame:
    """
    Загружает локальные исторические данные из Parquet.

    Args:
        ticker:
            Биржевой тикер.

        interval:
            Таймфрейм.

    Returns:
        DataFrame с историческими OHLCV-данными.

    Raises:
        FileNotFoundError:
            Если файл отсутствует.
    """

    file_path = MARKET_DATA_DIR / f"{ticker}_{interval}.parquet"

    return pd.read_parquet(file_path)