@echo off
REM Demo Launcher - Opens new terminal and starts the demo recording script
REM Double-click this file to start the Platinum Tier demo

echo ========================================
echo Platinum Tier AI Employee Demo Launcher
echo ========================================
echo.
echo This will open a new PowerShell window and start the demo.
echo Make sure you have your screen recorder ready!
echo.
pause

start powershell.exe -ExecutionPolicy Bypass -NoExit -Command "Set-Location 'C:\HACKATHON 0'; & '.\record_demo.ps1'"
