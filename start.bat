@echo off
echo ===============================
echo   Starting Redis in Docker...
echo ===============================
docker-compose up -d

echo.
echo ===============================
echo   Launching Program...
echo ===============================
dist\main.exe

echo.
echo ===============================
echo   Program closed. Press any key to exit.
echo ===============================
pause