import enum

from telegram import Dice


class CombinationsEnum(int, enum.Enum):
    BARS = 1
    BERRIES = 22
    LEMONS = 43
    JACKPOT = 64

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))


class CasinoGameController:
    def __init__(self, config):
        self.config = config

    def check_win_condition(self, dice: Dice) -> bool:
        """Проверка условия победы по значению dice"""
        dice_value = dice.value
        dice_emoji = dice.emoji

        # Проверяем, что эмодзи соответствует настройкам
        if dice_emoji != self.config['dice_emoji']:
            return False

        if self.config['win_condition'] == 'slot_jackpot':
            # Три семерки
            return dice_value == CombinationsEnum.JACKPOT

        elif self.config['win_condition'] == 'specific_value':
            # Выигрыш по конкретным значениям
            return dice_value in self.config['target_values']

        elif self.config['win_condition'] == 'any_win':
            # Любая комбинация
            return dice_value in CombinationsEnum.values()

        elif self.config['win_condition'] == 'three_bars':
            # Три бара
            return dice_value == CombinationsEnum.BARS

        elif self.config['win_condition'] == 'three_lemons':
            # Три лемона
            return dice_value == CombinationsEnum.LEMONS

        elif self.config['win_condition'] == 'three_berries':
            # Три ягоды
            return dice_value == CombinationsEnum.BERRIES

        return False
