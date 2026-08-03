@echo off
chcp 65001 >nul
title Установка D.E.E.P. Assistant

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║      УСТАНОВЩИК D.E.E.P. ASSISTANT v2.0.7          ║
echo ╚══════════════════════════════════════════════════════╝
echo.

:: Проверка Python
echo [1/3] Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден!
    echo.
    echo Установите Python с https://www.python.org/downloads/
    echo При установке ОБЯЗАТЕЛЬНО отметьте "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
echo [OK] Python обнаружен.

:: Установка библиотек
echo.
echo [2/3] Установка библиотек...
python -m pip install --upgrade pip --quiet
python -m pip install requests duckduckgo-search deep-translator --quiet
echo [OK] Библиотеки установлены.

:: Создание ярлыка на рабочем столе
echo.
echo [3/3] Создание ярлыка...
set "SCRIPT_DIR=%~dp0"
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\DEEP Assistant.lnk"

:: Создаём VBS скрипт для ярлыка
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\create_shortcut.vbs"
echo sLinkFile = "%SHORTCUT%" >> "%TEMP%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create_shortcut.vbs"
echo oLink.TargetPath = "python.exe" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Arguments = """%SCRIPT_DIR%deep_assistant.py""" >> "%TEMP%\create_shortcut.vbs"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Description = "D.E.E.P. - Ретро ИИ-ассистент" >> "%TEMP%\create_shortcut.vbs"
echo oLink.WindowStyle = 1 >> "%TEMP%\create_shortcut.vbs"
echo oLink.Save >> "%TEMP%\create_shortcut.vbs"

cscript /nologo "%TEMP%\create_shortcut.vbs"
del "%TEMP%\create_shortcut.vbs"

echo [OK] Ярлык создан на рабочем столе.

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║             УСТАНОВКА ЗАВЕРШЕНА!                   ║
echo ╠══════════════════════════════════════════════════════╣
echo ║                                                    ║
echo ║  ВАЖНО! Перед первым запуском:                     ║
echo ║  1. Откройте файл deep_assistant.py                ║
echo ║  2. Найдите строку OPENROUTER_API_KEY              ║
echo ║  3. Замените "твой_ключ_сюда" на свой ключ        ║
echo ║                                                    ║
echo ║  Получить бесплатный ключ:                         ║
echo ║  https://openrouter.ai/keys                        ║
echo ║                                                    ║
echo ║  Для запуска используйте ярлык на рабочем столе    ║
echo ║  или команду: python deep_assistant.py             ║
echo ║                                                    ║
echo ╚══════════════════════════════════════════════════════╝
echo.
pause