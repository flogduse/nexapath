@echo off
title NexaPath - AI Career Copilot
echo ========================================
echo    NexaPath - AI Career Copilot
echo    Team PromptX | IBM SkillsBuild
echo ========================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -r requirements.txt --quiet

echo [2/3] Starting NexaPath server...
start /b python backend\app.py

timeout /t 3 /nobreak >nul

echo [3/3] Opening NexaPath in browser...
start "" "%~dp0frontend\index.html"

echo.
echo ========================================
echo  NexaPath is running!
echo  Frontend: frontend\index.html
echo  API: http://localhost:5000
echo  Close this window to stop the server.
echo ========================================
echo.
pause
