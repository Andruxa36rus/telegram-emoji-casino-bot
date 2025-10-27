import asyncio
import logging
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional
import sys

from telegram.ext import CommandHandler
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from application.setup import ApplicationBuilder


def main():
    """Основная функция запуска"""

    # Создание контроллера с основной логикой приложения
    controller = ApplicationBuilder.build()

    # Создание приложения (бот телеграм)
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Регистрация обработчиков
    # application.add_handler(CommandHandler("start", app.start_command))
    application.add_handler(CommandHandler("status", controller.status_command))
    application.add_handler(MessageHandler(filters.Dice.ALL, controller.handle_dice))
    application.add_error_handler(controller.error_handler)

    # Запуск бота
    print("✅ Бот запущен")
    print("Конфигурация:")
    print(f"  Режим: {controller.config['dice_emoji']}")
    print(f"  Условие победы: Выбить `{controller.config['win_condition']}` {controller.config['wins_needed']} раз(-а)")
    print(f"  Сообщение победы: `{controller.config['win_condition']}`")
    print(f"  Сообщение комбинации: `{controller.config['progress_message']}`")
    print(f"  Сообщение об окончании игры: `{controller.config['stop_message']}`")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    main()
