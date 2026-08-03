@echo off
chcp 65001 >nul
title Установка библиотек D.E.E.P. Assistant
cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║      УСТАНОВКА БИБЛИОТЕК D.E.E.P.                  ║
echo ╚══════════════════════════════════════════════════════╝
echo.

echo [*] Установка библиотек...
echo.

python -m pip install --user requests duckduckgo-search deep-translator SpeechRecognition pyttsx3 pystray pillow keyboard flask

if %errorlevel% neq 0 (
    echo.
    echo [!] Ошибка! Пробуем альтернативный способ...
    py -m pip install --user requests duckduckgo-search deep-translator SpeechRecognition pyttsx3 pystray pillow keyboard flask
)

if %errorlevel% neq 0 (
    echo.
    echo [!] Ошибка! Пробуем без --user...
    python -m pip install requests duckduckgo-search deep-translator SpeechRecognition pyttsx3 pystray pillow keyboard flask
)

echo.
echo [OK] Установка завершена.
timeout /t 3 >nul