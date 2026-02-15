@echo off
REM AI Employee - Bronze Tier Setup Script (Windows)
REM This script sets up the environment for the Bronze tier implementation

echo ==========================================
echo AI Employee - Bronze Tier Setup
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo [OK] Python version OK
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed
echo.

REM Create environment file
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env >nul

    REM Set default paths
    set VAULT_DIR=%CD%\AI_Employee_Vault

    echo VAULT_INBOX=%VAULT_DIR%\Inbox >> .env
    echo VAULT_NEEDS_ACTION=%VAULT_DIR%\Needs_Action >> .env
    echo VAULT_DONE=%VAULT_DIR%\Done >> .env

    echo [OK] .env file created
) else (
    echo .env file already exists, skipping...
)
echo.

REM Create vault structure
echo Creating vault folder structure...
if not exist "%VAULT_DIR%\Inbox" mkdir "%VAULT_DIR%\Inbox"
if not exist "%VAULT_DIR%\Needs_Action" mkdir "%VAULT_DIR%\Needs_Action"
if not exist "%VAULT_DIR%\Done" mkdir "%VAULT_DIR%\Done"
if not exist "%VAULT_DIR%\Pending_Approval" mkdir "%VAULT_DIR%\Pending_Approval"

echo [OK] Vault structure created at %VAULT_DIR%
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next Steps:
echo 1. Review and customize .env file
echo 2. Start the file system watcher:
echo    venv\Scripts\activate
echo    python watchers\filesystem_watcher.py
echo.
echo 3. In another terminal, process tasks:
echo    venv\Scripts\activate
echo    python skills\process_tasks.py --process
echo.
echo 4. Update dashboard:
echo    venv\Scripts\activate
echo    python skills\update_dashboard.py
echo.
echo For more information, see QUICKSTART.md
echo.
pause
