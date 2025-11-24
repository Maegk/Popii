@echo off
REM Creative Fatigue Detection System - Auto Start Script for Windows
REM Double-click this file to start the application

echo ==================================================
echo   Creative Fatigue Detection System
echo   Starting application...
echo ==================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Docker is not installed. Please install Docker Desktop first.
    echo   Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [OK] Docker is installed
echo.

REM Start services with Docker Compose
echo [*] Starting services...
docker-compose up -d

if %errorlevel% neq 0 (
    echo X Failed to start services. Make sure Docker Desktop is running.
    pause
    exit /b 1
)

echo.
echo [*] Waiting for services to start (30-60 seconds)...
timeout /t 15 /nobreak >nul

echo [*] Checking backend...
timeout /t 10 /nobreak >nul

echo [OK] Services are starting...
echo.

echo ==================================================
echo   Application is ready!
echo ==================================================
echo.
echo   Frontend UI:  http://localhost:3000
echo   Backend API:  http://localhost:8000
echo   API Docs:     http://localhost:8000/docs
echo.
echo   Opening browser in 3 seconds...
echo.
echo   To stop: Close this window or run stop.bat
echo ==================================================

timeout /t 3 /nobreak >nul

REM Open browser
start http://localhost:3000

echo.
echo Application is running. Do not close this window.
echo Press Ctrl+C to stop the application.
echo.

REM Show logs
docker-compose logs -f
