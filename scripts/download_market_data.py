"""
scripts.download_market_data
============================

Утилита для загрузки исторических рыночных данных.

Назначение:
    Скачивает исторические данные через yfinance и сохраняет их
    локально в формате Parquet.

    Используется для:
        - тестирования алгоритмов без подключения к Yahoo Finance;
        - проверки работы сканера в выходные и праздничные дни;
        - создания набора исторических данных для разработки.

Использование:
    python -m scripts.download_market_data
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yfinance as yf

from config import MARKET_DATA_DIR


# =============================================================================
# Settings
# =============================================================================

TICKERS = [
    "NTNX",
    "OMDA",
]

PERIOD = "5d"
INTERVAL = "5m"


# =============================================================================
# Functions
# =============================================================================

def download_market_data(
    ticker: str,
    period: str = PERIOD,
    interval: str = INTERVAL,
) -> None:
    """
    Загружает исторические данные по одному тикеру
    и сохраняет их в формате Parquet.

    Args:
        ticker:
            Биржевой тикер.

        period:
            Исторический период.

        interval:
            Таймфрейм свечей.

    Returns:
        None
    """

    print(f"Downloading {ticker}...")

    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
    )

    if df.empty:
        print(f"✗ No data received for {ticker}")
        return

    # yfinance иногда возвращает MultiIndex.
    df.columns = [
        column[0] if isinstance(column, tuple) else column
        for column in df.columns
    ]

    MARKET_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = MARKET_DATA_DIR / f"{ticker}_{interval}.parquet"

    df.to_parquet(file_path)

    print(
        f"✓ Saved: {file_path.name} "
        f"({len(df)} candles)"
    )


def main() -> None:
    """
    Загружает данные для всех тикеров.
    """

    print("=" * 50)
    print("Downloading historical market data")
    print("=" * 50)

    for ticker in TICKERS:
        download_market_data(ticker)

    print("\nDone.")


if __name__ == "__main__":
    main()