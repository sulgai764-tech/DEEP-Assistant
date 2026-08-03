@echo off
chcp 65001 >nul 2>&1
title D.E.E.P. Web Server
cd /d "%~dp0"
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║        D.E.E.P. WEB SERVER                           ║
echo ╚══════════════════════════════════════════════════════╝
echo.
python server.py
pause