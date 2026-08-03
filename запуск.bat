@echo off
chcp 65001 >nul 2>&1
title D.E.E.P. Assistant - Управление

:: Проверка прав администратора для автозагрузки
net session >nul 2>&1
set ADMIN=%errorlevel%

cd /d "%~dp0"

:menu
cls
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║          D.E.E.P. ASSISTANT - УПРАВЛЕНИЕ           ║
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
echo.
echo [*] Запуск D.E.E.P. Assistant...
echo.
python deep_assistant.py
goto end

:add_autostart
cls
echo.
echo [*] Добавление в автозагрузку Windows...

:: Создаём VBS-скрипт для скрытого запуска
echo Set WshShell = CreateObject("WScript.Shell") > "%~dp0launch_deep.vbs"
echo WshShell.Run "cmd /c cd /d %~dp0 && python deep_assistant.py", 0, False >> "%~dp0launch_deep.vbs"

:: Добавляем в реестр (автозагрузка для текущего пользователя)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DEEP_Assistant" /t REG_SZ /d "wscript.exe \"%~dp0launch_deep.vbs\"" /f >nul 2>&1

if %errorlevel% equ 0 (
    echo.
    echo ╔══════════════════════════════════════════════════════╗
    echo ║  [OK] Ассистент добавлен в автозагрузку!           ║
    echo ║                                                    ║
    echo ║  Теперь D.E.E.P. Assistant будет запускаться       ║
    echo ║  автоматически при включении компьютера.           ║
    echo ║                                                    ║
    echo ║  Окно будет скрыто. Чтобы открыть:                 ║
    echo ║  - Запустите этот файл и выберите пункт 1          ║
    echo ╚══════════════════════════════════════════════════════╝
) else (
    echo.
    echo [ОШИБКА] Не удалось добавить в автозагрузку.
    echo Запустите файл от имени администратора!
)
echo.
pause
goto menu

:remove_autostart
cls
echo.
echo [*] Удаление из автозагрузки Windows...

reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "DEEP_Assistant" /f >nul 2>&1
del "%~dp0launch_deep.vbs" >nul 2>&1

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║  [OK] Ассистент удалён из автозагрузки!            ║
echo ║  Теперь он не будет запускаться при включении ПК.  ║
echo ╚══════════════════════════════════════════════════════╝
echo.
pause
goto menu

:run_and_add
cls
echo [*] Добавление в автозагрузку и запуск...
call :add_autostart
echo.
echo [*] Запуск ассистента...
start "" python "%~dp0deep_assistant.py"
goto end

:end
echo.
echo Нажмите любую клавишу для выхода...
pause >nul
exit /b 0