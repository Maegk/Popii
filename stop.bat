@echo off
REM Creative Fatigue Detection System - Stop Script for Windows

echo ==================================================
echo   Stopping Creative Fatigue Detection System...
echo ==================================================
echo.

docker-compose down

echo.
echo [OK] Application stopped successfully!
echo.
pause
