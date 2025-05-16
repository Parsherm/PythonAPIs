@echo off
echo ===============================
echo   Starting Redis in Docker...
echo ===============================
docker-compose up -d

echo.
echo ===============================
echo   Launching Program...
echo ===============================
python ./main.py

echo.
echo ===============================
echo   Program closed. Press any key to exit.
echo ===============================
pause