"""
monitor.notifier
================

Модуль для отправки пользовательских уведомлений.

Назначение:
    Предоставляет единый интерфейс для отображения уведомлений.
    На текущем этапе поддерживаются только системные уведомления Linux.
    ``notify-send``.

    В дальнейшем модуль может быть расширен поддержкой:
        - Telegram;
        - Discord;
        - электронной почты;
        - звуковых уведомлений.

Использование:
    >>> from monitor.notifier import notify
    >>> notify(
    ...     title="Stock Monitor",
    ...     message="RKLB entered 5m consolidation."
    ... )
"""

from __future__ import annotations

import os
import shutil
import subprocess


def play_sound() -> None:
    """
    Воспроизводит системный звуковой сигнал.

    Используется как часть пользовательского уведомления.
    """

    try:
        subprocess.run(
            ["canberra-gtk-play", "--id=complete"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
    )
    except Exception:
        pass


def notify(
    title: str,
    message: str,
    timeout: int = 8000,
) -> None:
    """
    Отображает системное уведомление в Linux.

    Для показа уведомлений используется утилита ``notify-send``,
    входящая в пакет ``libnotify``.

    Отправляет пользовательское уведомление.

    На текущем этапе уведомление состоит из:
    - системного уведомления Linux (notify-send);
    - звукового сигнала (canberra-gtk-play).

    Args:
        title (str):
            Заголовок уведомления.

        message (str):
            Основной текст уведомления.

        timeout (int, optional):
            Время отображения уведомления в миллисекундах.
            По умолчанию 8000 (8 секунд).

    Returns:
        None

    Raises:
        RuntimeError:
            Если утилита ``notify-send`` отсутствует в системе.

        subprocess.SubprocessError:
            Если произошла ошибка во время запуска процесса.

    Examples:
        >>> notify(
        ...     title="5m Consolidation",
        ...     message="RKLB"
        ... )

        >>> notify(
        ...     title="Breakout",
        ...     message="CRDO",
        ...     timeout=12000,
        ... )
    """

    # Проверяем наличие системной утилиты notify-send.
    if shutil.which("notify-send") is None:
        raise RuntimeError(
            "System utility 'notify-send' was not found. "
            "Install package 'libnotify-bin'."
        )

    # subprocess.run(
    #     [
    #         "notify-send",
    #         "-t",
    #         str(timeout),
    #         title,
    #         message,
    #     ],
    #     check=True,
    #     capture_output=True,
    #     text=True,
    # )
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    env["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"

    try:
        subprocess.run(
            [
                "notify-send",
                "-t",
                str(timeout),
                title,
                message,
            ],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
    except subprocess.CalledProcessError as error:
        print(f"[notify-send] {error.stderr.strip()}")



    play_sound()