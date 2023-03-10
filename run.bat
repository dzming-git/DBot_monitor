@echo off
set PYTHON_PATH="D:\anaconda3\envs\qqbot_env\python.exe"
start "" /D "." cmd /K "title DBot_monitor & %PYTHON_PATH% -m app.server"
