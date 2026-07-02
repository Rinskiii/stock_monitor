"""
monitor.storage
===============

Модуль для хранения состояния мониторинга.

Назначение:
    Предоставляет единый интерфейс для чтения и сохранения текущих
    торговых сигналов. На данный момент используется JSON-файл
    ``data/alerts.json``.

Использование:
    >>> from monitor.storage import load_alerts, save_alerts
    >>>
    >>> alerts = load_alerts()
    >>> alerts.add("AAPL")
    >>> save_alerts(alerts)

Особенности:
    - При первом запуске автоматически создаёт файл хранения.
    - Возвращает множество (set), что упрощает сравнение сигналов
      между запусками программы.
    - Не зависит от логики сканирования или уведомлений.
"""

from __future__ import annotations

import json
from pathlib import Path

import config


def load_alerts() -> set[str]:
    """
    Загружает ранее сохранённые сигналы мониторинга.

    Если файл ``alerts.json`` отсутствует, он автоматически создаётся
    с пустым списком сигналов.

    Returns:
        set[str]:
            Множество тикеров, находящихся в состоянии активного сигнала.

    Raises:
        json.JSONDecodeError:
            Если файл существует, но содержит некорректный JSON.

        OSError:
            Если возникла ошибка при работе с файловой системой.

    Examples:
        >>> load_alerts()
        {'RKLB', 'CRDO'}

        >>> load_alerts()
        set()
    """
    alerts_path = Path(config.ALERTS_FILE)

    # При первом запуске создаём файл с пустым списком сигналов.
    if not alerts_path.exists():
        alerts_path.parent.mkdir(parents=True, exist_ok=True)
        alerts_path.write_text("[]", encoding="utf-8")
        return set()

    with alerts_path.open("r", encoding="utf-8") as file:
        alerts = json.load(file)

    return set(alerts)


def save_alerts(alerts: set[str]) -> None:
    """
    Сохраняет текущее состояние активных сигналов.

    Данные сохраняются в формате JSON с сортировкой по алфавиту,
    что делает файл более читаемым и удобным для контроля версий.

    Args:
        alerts (set[str]):
            Множество тикеров, находящихся в состоянии активного сигнала.

    Returns:
        None

    Raises:
        OSError:
            Если произошла ошибка при записи файла.

    Examples:
        >>> save_alerts({"RKLB", "CRDO"})
    """
    alerts_path = Path(config.ALERTS_FILE)

    alerts_path.parent.mkdir(parents=True, exist_ok=True)

    with alerts_path.open("w", encoding="utf-8") as file:
        json.dump(
            sorted(alerts),
            file,
            indent=4,
            ensure_ascii=False,
        )