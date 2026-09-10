@echo off
start python main.py
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000/login.html
exit