@echo off
echo Setting up Flex-CRM...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is required but not installed. Please install Python and try again.
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is required but not installed. Please install pip and try again.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    if exist .env.example (
        copy .env.example .env
    ) else (
        echo SECRET_KEY=demo-key-please-change-in-production > .env
    )
)

REM Initialize database
echo Initializing database...
python database/create_db.py

echo.
echo Setup complete! You can now run the application with:
echo venv\Scripts\activate.bat
echo python main.py
echo.
echo The application will be available at http://localhost:8000
