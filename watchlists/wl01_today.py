"""
watchlists.wl01_today
=====================

Основной список акций для ежедневного мониторинга.

Использование:
    >>> from watchlists.wl01_today import get_watchlist
    >>> tickers = get_watchlist()
"""

from __future__ import annotations


def get_watchlist() -> list[str]:
    """
    Возвращает список тикеров для ежедневного мониторинга.

    Returns:
        Список тикеров.
    """

    return sorted(
        {
            "RKLB",
            "CRDO",
            "PLTR",
            "TEM",
            "NBIS",
        }
    )