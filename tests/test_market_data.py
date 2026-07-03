"""
tests.test_market_data
======================

Тест загрузки локальных исторических данных.

Назначение:
    Проверяет, что файл с историческими данными успешно читается
    из директории ``data/market_data`` и имеет ожидаемую структуру.

    Тест выводит:
        - количество свечей;
        - дату первой свечи;
        - дату последней свечи;
        - первые строки DataFrame;
        - последние строки DataFrame;
        - информацию о столбцах.

Использование:
    python -m tests.test_market_data
"""

from __future__ import annotations

import pandas as pd

from config import MARKET_DATA_DIR


def load_market_data(
    ticker: str,
    interval: str = "5m",
) -> pd.DataFrame:
    """
    Загружает локальные исторические данные.

    Args:
        ticker:
            Биржевой тикер.

        interval:
            Таймфрейм.

    Returns:
        DataFrame с историческими данными.

    Raises:
        FileNotFoundError:
            Если файл отсутствует.
    """

    file_path = MARKET_DATA_DIR / f"{ticker}_{interval}.parquet"

    return pd.read_parquet(file_path)


def main() -> None:
    """
    Проверяет чтение локального файла с историческими данными.
    """

    ticker = "NTNX"

    df = load_market_data(ticker)

    print("=" * 60)
    print(f"{ticker} ({len(df)} candles)")
    print("=" * 60)

    print(f"First candle : {df.index.min()}")
    print(f"Last candle  : {df.index.max()}")

    print("\nDataFrame shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nLast 5 rows:")
    print(df.tail())

    print("\nDataFrame info:")
    df.info()


if __name__ == "__main__":
    main()