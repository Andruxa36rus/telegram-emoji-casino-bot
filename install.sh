#!/bin/bash

# setup.sh
# Скрипт для настройки окружения бота казино

echo "==================================="
echo "Настройка окружения Casino Bot"
echo "==================================="

# Установка virtualenv через pip
echo "📦 Установка virtualenv..."
pip install virtualenv

# Создание виртуального окружения
echo "🐍 Создание виртуального окружения 'casino_bot_env'..."
virtualenv casino_bot_env

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source casino_bot_env/bin/activate

# Обновление pip до последней версии
echo "⬆️ Обновление pip..."
pip install --upgrade pip

# Установка зависимостей
if [ -f "requirements.txt" ]; then
    echo "📥 Установка зависимостей из requirements.txt..."
    pip install -r requirements.txt
else
    echo "⚠️ Файл requirements.txt не найден!"
    echo "Создайте файл requirements.txt с необходимыми зависимостями."
fi

echo ""
echo "==================================="
echo "✅ Настройка завершена!"
echo "==================================="
echo ""
echo "Для активации окружения выполните:"
echo "source casino_bot_env/bin/activate"
echo ""
echo "Для деактивации выполните:"
echo "deactivate"
echo ""

# Оставляем терминал открытым (аналог pause в Windows)
read -p "Нажмите Enter для выхода..."
