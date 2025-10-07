import datetime
import sys
import os
from pathlib import Path
import typing
import json
from application.games.casino import CasinoGameController
from application.controller import ApplicationController
from application.logger import setup_logger

ROOT_PATH = Path(__file__).parent.parent


class ApplicationBuilder:
    config_path = ROOT_PATH / 'config.json'
    log_dir = ROOT_PATH / 'logs' / datetime.datetime.now().strftime("%H-%M-%S_%Y-%m-%d")
    env_file = ROOT_PATH / '.env'

    @classmethod
    def build(cls):
        from dotenv import load_dotenv
        print(cls.env_file)
        load_dotenv(dotenv_path=cls.env_file)
        cls.check_health()
        config = cls.load_config()
        app = ApplicationController(config)
        # TODO регистрировать игру в соответствии с конфигурацией (кости/дартс/казик)
        app.register_game(CasinoGameController(config))
        app.register_logger(*setup_logger(cls.log_dir))
        return app

    @staticmethod
    def check_health():
        # Проверка, что все зависимости установлены
        try:
            from telegram import Bot, Update, Dice
            from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
            from telegram.constants import ChatAction
            from dotenv import load_dotenv
        except ImportError as e:
            print(f"Ошибка импорта {e}")
            print("Убедитесь, что установлены все зависимости: pip install -r requirements.txt")
            sys.exit(1)
        # Проверка переменных окружения
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            print("Ошибка: Не установлена переменная окружения TELEGRAM_BOT_TOKEN!")
            print("Установите: TELEGRAM_BOT_TOKEN=your_bot_token_here")
            sys.exit(1)

    @classmethod
    def _create_default_config(cls) -> typing.Dict:
        """Создание конфигурации по умолчанию"""
        default_config = {
            "win_condition": "slot_jackpot",  # slot_jackpot, specific_value, any_win
            "wins_needed": 2,
            "dice_emoji": "🎰",  # 🎲, 🎯, 🎳, 🏀, ⚽, 🎰
            "target_values": [64],  # Для 🎰: 64 - джекпот
            "win_message": "🎉 Поздравляем! Вы выиграли! 🎉",
            "stop_message": "⛔ Игра завершена! Победитель уже определен!",
            "progress_message": "{count} побед"
        }

        with open(cls.config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)

        print(f"Создан файл конфигурации по умолчанию: {cls.config_path}")
        return default_config

    @classmethod
    def load_config(cls) -> typing.Dict:
        """Загрузка конфигурации из JSON файла"""
        try:
            with open(cls.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Валидация конфигурации
            required_fields = ['win_condition', 'wins_needed', 'dice_emoji',
                               'target_values', 'win_message', 'stop_message',
                               'progress_message']

            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Отсутствует обязательное поле в конфиге: {field}")

            return config

        except FileNotFoundError:
            print(f"Файл конфигурации {cls.config_path} не найден!")
            print("Создаю файл с конфигурацией по умолчанию...")
            return cls._create_default_config()
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            sys.exit(1)
