@echo off
pip install virtualenv
virtualenv casino_bot_env
call casino_bot_env\Scripts\activate.bat
pip install -r requirements.txt
pause