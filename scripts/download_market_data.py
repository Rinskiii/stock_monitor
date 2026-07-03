"""
scripts.download_market_data
============================

Утилита для загрузки исторических рыночных данных.

Назначение:
    Скачивает исторические данные через Yahoo Finance и сохраняет их
    локально в формате Parquet.

    Используется для:
        - тестирования алгоритмов без подключения к Yahoo Finance;
        - проверки работы сканера в выходные и праздничные дни;
        - создания набора исторических данных для разработки.

Использование:
    python -m scripts.download_market_data
"""

from __future__ import annotations

from monitor.data_source import download_from_yahoo

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


def main() -> None:
    """
    Загружает данные для всех тикеров и сохраняет их в Parquet.
    """

    print("=" * 50)
    print("Downloading historical market data")
    print("=" * 50)

    MARKET_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for ticker in TICKERS:
        print(f"Downloading {ticker}...")

        df = download_from_yahoo(
            ticker=ticker,
            period=PERIOD,
            interval=INTERVAL,
        )

        file_path = MARKET_DATA_DIR / f"{ticker}_{INTERVAL}.parquet"

        df.to_parquet(file_path)

        print(f"Saved -> {file_path.name}")

    print("\nDone.")


if __name__ == "__main__":
    main()