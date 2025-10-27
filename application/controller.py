import typing
from datetime import datetime
from telegram import Bot, Update, Dice
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction


class ApplicationController:
    def __init__(self, config):
        # Победители
        self.winners = {}
        self.username_map = {}
        # После остановки игры, победители больше не фиксируются
        self.game_active = True
        # Конфигурация
        self.config: typing.Dict = config
        # Кеш обработанных сообщений
        self.processed_messages: typing.Set[int] = set()

    @classmethod
    def register_game(cls, game_controller):
        cls.game_controller = game_controller

    @classmethod
    def register_logger(cls, winner, error):
        # Логирование
        cls.winners_logger = winner
        cls.error_logger = error

    async def handle_dice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ Обработка сообщения """
        if not self.game_active:
            # Игра завершена, отправляем стоп-сообщение
            stop_message = self.config['stop_message']
            await self.send_reply(update, stop_message)
            return
        message = update.message
        user_id = message.from_user.id
        username = message.from_user.username
        dice = message.dice

        if message.forward_origin:
            return

        # Проверяем, не обрабатывали ли уже это сообщение
        if message.message_id in self.processed_messages:
            return
        # Записываем принятое сообщение в кеш уже обработанных сообщений
        self.processed_messages.add(message.message_id)

        # Проверяем условие победы
        if self.game_controller.check_win_condition(dice):
            win_time = datetime.now()

            # Логируем победу
            self.log_winner(user_id, username, win_time, dice.value, message.message_id)

            # Получаем количество побед пользователя
            win_count = len(self.winners.get(user_id, []))

            if win_count >= self.config['wins_needed']:
                # Пользователь достиг нужного количества побед
                self.game_active = False
                win_message = self.config['win_message']
                await self.send_reply(update, win_message)
                print(f"Игра завершена! Победитель: @{username if username else user_id}")

            else:
                # Пользователь еще не достиг нужного количества побед
                progress_msg = self.config['progress_message'].format(count=win_count)
                await self.send_reply(update, progress_msg)

    async def send_reply(self, update: Update, message: str):
        """ Отправка ответа на сообщение """
        try:
            await update.message.reply_text(message)
        except Exception as e:
            self.error_logger.error(f"Ошибка отправки сообщения: {e}")

    def log_winner(self, user_id: int, username: str, win_time: datetime, dice_value: int, message_id: int):
        """ Логирование победителя """
        user_mention = f"@{username}" if username else f"id{user_id}"
        self.winners.setdefault(user_id, [])

        win_data = {
            "datetime": win_time,
            "value": dice_value,
            "message_id": message_id
        }
        self.winners[user_id].append(win_data)
        self.username_map[user_id] = user_mention

        # Запись в лог
        times_str = ', '.join([f"{dt['datetime'].strftime('%Y-%m-%d %H:%M:%S')}(выпало:{dt['value']})"
                               for dt in self.winners[user_id]])
        log_entry = f"{user_mention}: [{times_str}] ID сообщения: {message_id}"

        self.winners_logger.info(log_entry)
        print(f"Записан победитель: {log_entry}")

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ Обработчик ошибок """
        self.error_logger.error(f"Ошибка: {context.error}")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /status"""
        status_text = (
            f"📊 Статус игры:\n"
            f"- Игра активна ✅\n" if self.game_active else "Игра завершена ⛔\n"
            f"- Текущие лидеры:\n"
        )

        # Добавляем информацию о топ-победителях
        sorted_winners = sorted(self.winners.items(), key=lambda x: len(x[1]), reverse=True)#[:5]
        for i, (user_id, wins) in enumerate(sorted_winners, 1):
            username = "Неизвестно"
            # Пытаемся получить username из контекста
            if wins:
                user_mention = self.username_map.get(user_id, f"id{user_id}")
                message_links = []
                for win in wins:
                    message_links.append(f"https://t.me/logovoboica/{win.get('message_id', 'ошибка')}")
                links_string = "\n".join(message_links)
                status_text += f"{i}. {user_mention}: {len(wins)} побед\n{links_string}\n\n"

        await self.send_reply(update, status_text)