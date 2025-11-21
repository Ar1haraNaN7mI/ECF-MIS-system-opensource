@echo off
echo ====================================
echo MIS System Environment Setup
echo ====================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

echo [3/4] Upgrading pip...
python -m pip install --upgrade pip
echo.

echo [4/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.
echo ====================================
echo Environment setup completed!
echo ====================================
echo.
echo To activate the environment in the future, run:
echo   venv\Scripts\activate.bat
echo.
echo To start the application, run:
echo   python app.py
echo.
pause



