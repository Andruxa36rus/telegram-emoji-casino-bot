@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ========================================
echo    Запуск бота для казино Telegram
echo ========================================
echo.

set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%casino_bot_env"
set "MAIN_SCRIPT=%ROOT_DIR%main.py"

echo Проверка виртуального окружения...
if not exist "!VENV_DIR!" (
    echo Виртуальное окружение не найдено!
    echo Выполните установку: install.bat
    pause
    exit /b 1
)

echo Проверка основного скрипта...
if not exist "!MAIN_SCRIPT!" (
    echo Основной скрипт main.py не найден!
    echo Убедитесь, что он находится в папке: !ROOT_DIR!
    pause
    exit /b 1
)

echo Проверка переменных окружения...
set "TOKEN=%TELEGRAM_BOT_TOKEN%"
if "!TOKEN!"=="" (
    echo.
    echo ОШИБКА: Переменная окружения TELEGRAM_BOT_TOKEN не установлена!
    echo.
    echo Установите переменную окружения командой:
    echo set TELEGRAM_BOT_TOKEN=ваш_токен_бота
    echo.
    echo Или установите её временно в этом окне:
    set /p TELEGRAM_BOT_TOKEN="Введите токен бота: "
    if "!TELEGRAM_BOT_TOKEN!"=="" (
        echo Токен не введен! Запуск невозможен.
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Активация виртуального окружения...
echo ========================================
echo.

call "!VENV_DIR!\Scripts\activate.bat"

echo Проверка зависимостей...
python -c "import telegram" >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Зависимости не установлены!
    echo Выполните: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ========================================
echo Запуск бота...
echo ========================================
echo.

echo Токен бота: !TELEGRAM_BOT_TOKEN!
echo.
echo Если бот не запускается, проверьте:
echo 1. Корректность токена
echo 2. Наличие интернет-соединения
echo 3. Файл config.json в корневой папке
echo.
echo Для остановки бота нажмите Ctrl+C
echo.

python "!MAIN_SCRIPT!"

echo.
echo Бот завершил работу.
pause