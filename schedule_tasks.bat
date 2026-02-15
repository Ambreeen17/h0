@echo off
REM Scheduled Task Runner - Silver Tier Automation
REM Windows Task Scheduler compatible script

echo ==========================================
echo AI Employee - Scheduled Task Runner
echo ==========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run scheduled tasks
echo [%DATE% %TIME%] Running scheduled tasks...

REM 1. Generate plans for complex tasks
echo [1/4] Generating plans for complex tasks...
python skills\plan_generator.py --all

REM 2. Process pending tasks
echo [2/4] Processing pending tasks...
python skills\process_tasks.py --process

REM 3. Update dashboard
echo [3/4] Updating dashboard...
python skills\update_dashboard.py

REM 4. Check for approval requests
echo [4/4] Checking approval requests...
python skills\approval_workflow.py --stats

echo.
echo [%DATE% %TIME%] Scheduled tasks completed
echo ==========================================
echo.

pause
