@echo off
chcp 65001 >nul 2>&1
title D.E.E.P. Assistant - Запуск
cd /d "%~dp0"

:menu
cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║          D.E.E.P. ASSISTANT - ЗАПУСК                ║
echo ╠══════════════════════════════════════════════════════╣
echo ║                                                    ║
echo ║  1 - Запустить ассистента сейчас                   ║
echo ║  2 - Добавить в автозагрузку Windows               ║
echo ║  3 - Удалить из автозагрузки Windows               ║
echo ║  4 - Запустить + Добавить в автозагрузку           ║
echo ║  5 - Выход                                         ║
echo ║                                                    ║
echo ╚══════════════════════════════════════════════════════╝
echo.

set /p choice="Выберите действие (1-5): "

if "%choice%"=="1" goto just_run
if "%choice%"=="2" goto add_autostart
if "%choice%"=="3" goto remove_autostart
if "%choice%"=="4" goto run_and_add
if "%choice%"=="5" exit /b 0
goto menu

:just_run
cls
python deep_assistant.py
goto end

:add_autostart
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DEEP_Assistant" /t REG_SZ /d "\"%~dp0запуск.bat\"" /f >nul 2>&1
echo [OK] Автозагрузка включена.
pause
goto menu

:remove_autostart
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DEEP_Assistant" /f >nul 2>&1
echo [OK] Автозагрузка отключена.
pause
goto menu

:run_and_add
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DEEP_Assistant" /t REG_SZ /d "\"%~dp0запуск.bat\"" /f >nul 2>&1
python deep_assistant.py
goto end

:end
pause