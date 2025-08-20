@echo off
cd /D "%~dp0"

git pull

.\.venv\Scripts\python.exe hell_snake.py