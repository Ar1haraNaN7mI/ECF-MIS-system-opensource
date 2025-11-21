@echo off
echo Starting MIS System...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Please run setup_env.bat first to set up the environment.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found. Using default configuration.
    echo.
)

REM Start the application
echo Starting Flask application...
python app.py



