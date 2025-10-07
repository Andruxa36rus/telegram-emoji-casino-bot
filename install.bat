@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ========================================
echo    Установка бота для казино Telegram
echo ========================================
echo.

set "ROOT_DIR=%~dp0"
set "VENV_DIR=%ROOT_DIR%casino_bot_env"
set "REQUIREMENTS=%ROOT_DIR%requirements.txt"

echo Проверка наличия Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python не найден в системе!
    echo.
    echo Установите Python 3.8 или выше с официального сайта:
    echo https://www.python.org/downloads/
    echo.
    echo Не забудьте отметить галочку "Add Python to PATH" при установке!
    echo.
    pause
    exit /b 1
)

echo.
for /f "tokens=2" %%I in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%I"
echo Найден Python версии: !PYTHON_VERSION!

echo.
echo Проверка версии Python...
for /f "tokens=1,2,3 delims=." %%a in ("!PYTHON_VERSION!") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
)

if !MAJOR! lss 3 (
    echo Ошибка: Требуется Python 3.8 или выше!
    echo Текущая версия: !PYTHON_VERSION!
    pause
    exit /b 1
)

if !MINOR! lss 8 (
    echo Ошибка: Требуется Python 3.8 или выше!
    echo Текущая версия: !PYTHON_VERSION!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Создание виртуального окружения...
echo ========================================
echo.

if exist "!VENV_DIR!" (
    echo Виртуальное окружение уже существует. Удаляем...
    rmdir /s /q "!VENV_DIR!"
)

python -m venv "!VENV_DIR!"
if %errorlevel% neq 0 (
    echo Ошибка при создании виртуального окружения!
    pause
    exit /b 1
)

echo Виртуальное окружение создано: !VENV_DIR!

echo.
echo ========================================
echo Активация окружения и установка зависимостей
echo ========================================
echo.

call "!VENV_DIR!\Scripts\activate.bat"

echo Обновление pip...
python -m pip install --upgrade pip

if exist "!REQUIREMENTS!" (
    echo Установка зависимостей из requirements.txt...
    pip install -r "!REQUIREMENTS!"
) else (
    echo Файл requirements.txt не найден, устанавливаем зависимости по умолчанию...
    pip install python-telegram-bot
    pip install nest-asyncio
    pip install uvloop

    echo Создание файла requirements.txt...
    echo python-telegram-bot>=20.0 > "!REQUIREMENTS!"
    echo nest-asyncio >> "!REQUIREMENTS!"
    echo uvloop >> "!REQUIREMENTS!"
)

echo.
echo ========================================
echo Создание необходимых файлов и папок
echo ========================================
echo.

if not exist "!ROOT_DIR%config.json" (
    echo Создание config.json...
    echo { > "!ROOT_DIR%config.json"
    echo   "win_condition": "slot_jackpot", >> "!ROOT_DIR%config.json"
    echo   "wins_needed": 2, >> "!ROOT_DIR%config.json"
    echo   "dice_emoji": "🎰", >> "!ROOT_DIR%config.json"
    echo   "target_values": [64], >> "!ROOT_DIR%config.json"
    echo   "win_message": "🎉 Поздравляем! Вы выиграли! 🎉", >> "!ROOT_DIR%config.json"
    echo   "stop_message": "⛔ Игра завершена! Победитель уже определен!", >> "!ROOT_DIR%config.json"
    echo   "progress_message": "{count} побед" >> "!ROOT_DIR%config.json"
    echo } >> "!ROOT_DIR%config.json"
)

if not exist "!ROOT_DIR%logs" (
    echo Создание папки logs...
    mkdir "!ROOT_DIR%logs"
)

echo.
echo ========================================
echo Установка завершена успешно!
echo ========================================
echo.
echo Созданы следующие файлы и папки:
echo - !VENV_DIR!
echo - !ROOT_DIR%config.json
echo - !ROOT_DIR%logs\
echo.
echo Перед запуском установите переменную окружения:
echo set TELEGRAM_BOT_TOKEN=ваш_токен_бота
echo.
echo Для запуска бота выполните: run.bat
echo.

pause