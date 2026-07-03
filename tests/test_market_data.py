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

from monitor.data_source import load_parquet


def main() -> None:
    """
    Проверяет чтение локального файла с историческими данными.
    """

    ticker = "NTNX"

    df = load_parquet(ticker)

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