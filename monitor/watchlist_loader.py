"""
monitor.watchlist_loader
========================

Модуль для загрузки списка тикеров, указанного в конфигурации проекта.

Назначение:
    Загружает watchlist, имя которого задано в ``config.py``.
    Использует динамический импорт, благодаря чему для смены списка
    достаточно изменить значение ``WATCHLIST_NAME`` без изменения кода.

Использование:
    >>> from monitor.watchlist_loader import load_watchlist
    >>> tickers = load_watchlist()
"""

from __future__ import annotations

from importlib import import_module

from config import WATCHLIST_NAME


def load_watchlist() -> list[str]:
    """
    Загружает watchlist, указанный в конфигурации проекта.

    Returns:
        list[str]:
            Список тикеров.

    Raises:
    ModuleNotFoundError:
        Если указанный watchlist не существует.

    AttributeError:
        Если в модуле отсутствует функция ``get_watchlist()``.

    TypeError:
        Если ``get_watchlist()`` возвращает некорректный тип
        или список содержит элементы, отличные от строк.
    """

    # Импортируем модуль watchlist по имени, указанному в конфигурации
    module = import_module(f"watchlists.{WATCHLIST_NAME}")

    # Проверяем наличие функции get_watchlist() в модуле
    watchlist = module.get_watchlist()

    if not isinstance(watchlist, list):
        raise TypeError("get_watchlist() must return list[str].")

    if not all(isinstance(ticker, str) for ticker in watchlist):
        raise TypeError("Watchlist must contain only ticker strings.")

    watchlist = [ticker.strip().upper() for ticker in watchlist]

    return watchlist
