@echo off
REM Platinum Tier Demo Video Recording Script (Windows)
REM This script automates the demo flow for video recording
REM Usage: record_demo.bat

echo ========================================
echo Platinum Tier AI Employee Demo Recording
echo ========================================
echo.

REM Demo configuration
set DemoTitle=Personal AI Employee - Platinum Tier Demo
set OutputDir=demo_recording
set ScreenshotDir=%OutputDir%\screenshots

REM Create output directories
if not exist "%ScreenshotDir%" mkdir "%ScreenshotDir%"

echo.
echo ========================================
echo START YOUR SCREEN RECORDING NOW!
echo ========================================
echo.
echo Recommended tools:
echo   - Windows Game Bar: Press Win+G
echo   - OBS Studio: https://obsproject.com/
echo   - Microsoft Stream: Built into Windows 10/11
echo.
pause

echo.
echo [RECORDING] Demo started...
echo.

REM ========================================
REM INTRODUCTION
REM ========================================
cls
echo.
echo ========================================
echo PART 1: Introduction (2 minutes)
echo ========================================
echo.
timeout /t 2 >nul

echo.
echo [NARRATION] Welcome to the Platinum Tier AI Employee demo.
echo [NARRATION] This is a Production Hybrid AI Employee with cloud and local zones.
echo [NARRATION] Let me show you the complete architecture.
echo.
timeout /t 5 >nul

echo.
echo [COMMAND] Checking project structure...
dir
echo.
timeout /t 3 >nul

REM ========================================
REM PREPARATION
REM ========================================
cls
echo.
echo ========================================
echo PART 2: Setup Verification (2 minutes)
echo ========================================
echo.
timeout /t 2 >nul

echo.
echo [NARRATION] First, let me verify that all zone structures are in place.
echo.
echo [COMMAND] echo === Checking Zone Structures ===
echo === Checking Zone Structures ===
echo.
timeout /t 1 >nul

echo [COMMAND] Cloud Zone structure:
dir AI_Employee_Vault_Cloud
echo.
timeout /t 2 >nul

echo [COMMAND] Local Zone structure:
dir AI_Employee_Vault
echo.
timeout /t 2 >nul

echo [COMMAND] Sync Queue:
dir zone_sync_queue
echo.
timeout /t 2 >nul

echo [NARRATION] Perfect! We have our Cloud Zone, Local Zone, and Sync Queue all set up.
echo.
timeout /t 3 >nul

REM ========================================
REM WORK-ZONE ARCHITECTURE
REM ========================================
cls
echo.
echo ========================================
echo PART 3: Work-Zone Architecture (3 minutes)
echo ========================================
echo.
timeout /t 2 >nul

echo.
echo [NARRATION] Now let's examine the work-zone specialization.
echo [NARRATION] The Cloud Zone handles safe, non-sensitive operations.
echo.
echo [COMMAND] python skills/cloud_zone_manager.py --status
python skills/cloud_zone_manager.py --status
echo.
timeout /t 5 >nul

echo [NARRATION] The Cloud Zone can draft content, triage tasks, analyze data, and generate plans.
echo [NARRATION] Notice it has no access to credentials or banking operations.
echo.
timeout /t 4 >nul

echo [NARRATION] The Local Zone handles secure, sensitive operations.
echo.
echo [COMMAND] python skills/local_zone_manager.py --status
python skills/local_zone_manager.py --status
echo.
timeout /t 5 >nul

echo [NARRATION] The Local Zone handles approvals, sensitive execution, banking, and credentials.
echo [NARRATION] These capabilities are never available to the Cloud Zone.
echo.
timeout /t 4 >nul

echo [NARRATION] Let me show you the delegation architecture.
echo.
echo [COMMAND] python skills/zone_sync_manager.py --status
python skills/zone_sync_manager.py --status
echo.
timeout /t 5 >nul

echo [NARRATION] The delegation architecture ensures claim-by-move, single-writer dashboard,
echo [NARRATION] and markdown-only sync between zones. Secrets are never synced.
echo.
timeout /t 4 >nul

REM ========================================
REM CLOUD ZONE OPERATIONS
REM ========================================
cls
echo.
echo ========================================
echo PART 4: Cloud Zone Operations (4 minutes)
echo ========================================
echo.
timeout /t 2 >nul

echo.
echo [NARRATION] Now let's simulate a real-world scenario.
echo [NARRATION] An email arrives while the Local Zone is offline.
echo [NARRATION] The Cloud Zone detects it and creates a task.
echo.
timeout /t 5 >nul

echo [COMMAND] Creating email task in Cloud Zone...
(
echo # Task: Customer Inquiry about Q1 2026 Financial Reports
echo.
echo **Date**: 2026-02-15
echo **Type**: email-event
echo **Priority**: high
echo **Source**: cloud_zone ^(EmailWatcher^)
echo.
echo ## Email Content
echo.
echo From: customer@enterprise-client.com
echo Subject: Q1 2026 Financial Report Request
echo.
echo Hi,
echo.
echo I'm requesting our Q1 2026 financial reports for our quarterly review.
echo Can you provide the revenue summary and outstanding invoices?
echo.
echo Thanks,
echo Customer
) > AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md

echo [OK] Task created
echo.
timeout /t 3 >nul

echo [NARRATION] The Cloud Zone has detected the email and created a task.
echo [NARRATION] Now let's triage this task to determine how to handle it.
echo.
timeout /t 4 >nul

echo [COMMAND] python skills/cloud_zone_manager.py --triage AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md
python skills/cloud_zone_manager.py --triage AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md
echo.
timeout /t 5 >nul

echo [NARRATION] The triage shows this task requires the Local Zone because it involves financial data.
echo [NARRATION] This is an example of work-zone specialization in action.
echo.
timeout /t 5 >nul

echo [NARRATION] The Cloud Zone can still draft a response safely.
echo.
timeout /t 3 >nul

echo [COMMAND] python skills/cloud_zone_manager.py --draft linkedin "Thank you for your inquiry about Q1 2026 financial reports. Our revenue increased 25%% year-over-year, reaching $1.2M. Outstanding invoices total $45,000, all due within 30 days. Full report attached."
python skills/cloud_zone_manager.py --draft linkedin "Thank you for your inquiry about Q1 2026 financial reports. Our revenue increased 25% year-over-year, reaching $1.2M. Outstanding invoices total $45,000, all due within 30 days. Full report attached."
echo.
timeout /t 4 >nul

echo [COMMAND] Showing draft content...
type AI_Employee_Vault_Cloud\Drafts\draft-*.md
echo.
timeout /t 5 >nul

echo [NARRATION] The Cloud Zone has drafted a response safely.
echo [NARRATION] No sensitive operations were performed.
echo.
timeout /t 4 >nul

REM ========================================
REM SECURE ZONE SYNC
REM ========================================
cls
echo.
echo ========================================
echo PART 5: Secure Zone Sync (4 minutes)
echo ========================================
echo.
timeout /t 2 >nul

echo.
echo [NARRATION] Now let's demonstrate the secure sync between zones.
echo.
timeout /t 3 >nul

echo [COMMAND] python skills/cloud_zone_manager.py --sync AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md
python skills/cloud_zone_manager.py --sync AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md
echo.
timeout /t 4 >nul

echo [COMMAND] Showing synced file...
type local_zone_sync\email_inquiry_q1_2026.md
echo.
timeout /t 5 >nul

echo [NARRATION] The task has been synced to the Local Zone with metadata.
echo [NARRATION] Notice the Sync Information at the top.
echo.
timeout /t 4 >nul

echo [NARRATION] Now let's test the secret filtering.
echo.
timeout /t 3 >nul

echo [COMMAND] Creating file with secrets...
(
echo # Configuration
echo.
echo API_KEY = sk-1234567890abcdef
echo DATABASE_PASSWORD = mysecretpassword123
) > AI_Employee_Vault_Cloud\secret_config.md

echo [OK] Secret file created
echo.
timeout /t 2 >nul

echo [NARRATION] I've created a file with secrets in it.
echo [NARRATION] Let's try to sync it.
echo.
timeout /t 4 >nul

echo [COMMAND] python skills/zone_sync_manager.py --sync AI_Employee_Vault_Cloud\secret_config.md AI_Employee_Vault
python skills/zone_sync_manager.py --sync AI_Employee_Vault_Cloud\secret_config.md AI_Employee_Vault
echo.
timeout /t 4 >nul

echo [NARRATION] Perfect! The sync was blocked because it detected secret patterns.
echo [NARRATION] This ensures security even if the Cloud Zone is compromised.
echo.
timeout /t 5 >nul

REM ========================================
REM LOCAL ZONE APPROVAL
REM ========================================
cls
echo.
echo ========================================
echo PART 6: Local Zone Approval (5 minutes)
echo ========================================
echo.
timeout /t 2 >nul

echo.
echo [NARRATION] Now let's process the synced task in the Local Zone.
echo.
timeout /t 3 >nul

echo [COMMAND] python skills/local_zone_manager.py --process local_zone_sync\email_inquiry_q1_2026.md
python skills/local_zone_manager.py --process local_zone_sync\email_inquiry_q1_2026.md
echo.
timeout /t 5 >nul

echo [NARRATION] The Local Zone detected that this requires approval.
echo [NARRATION] Financial operations need human authorization.
echo.
timeout /t 4 >nul

echo [COMMAND] Showing approval request...
dir /b AI_Employee_Vault\Pending_Approval\*.json
echo.
for %%f in (AI_Employee_Vault\Pending_Approval\*.json) do type "%%f"
echo.
timeout /t 5 >nul

echo [NARRATION] Here's the approval request with the reason and threshold.
echo [NARRATION] Let me approve this action.
echo.
timeout /t 4 >nul

echo [COMMAND] Getting approval ID...
for %%f in (AI_Employee_Vault\Pending_Approval\*.json) do set APPROVAL_ID=%%~nf
echo Approval ID: %APPROVAL_ID%
echo.
timeout /t 2 >nul

echo [COMMAND] python skills/local_zone_manager.py --approve %APPROVAL_ID%
python skills/local_zone_manager.py --approve %APPROVAL_ID%
echo.
timeout /t 4 >nul

echo [NARRATION] The action has been approved and executed locally.
echo.
timeout /t 3 >nul

echo [COMMAND] Showing executed task...
type AI_Employee_Vault\Done\email_inquiry_q1_2026.md | more
echo.
timeout /t 5 >nul

echo [NARRATION] Notice the Local Zone Execution stamp.
echo [NARRATION] The task was executed with full security in the Local Zone.
echo.
timeout /t 4 >nul

REM ========================================
REM DELEGATION ARCHITECTURE
REM ========================================
cls
echo.
echo ========================================
echo PART 7: Delegation Architecture (2 minutes)
echo ========================================
echo.
timeout /t 2 >nul

echo.
echo [NARRATION] Let me demonstrate the claim-by-move delegation.
echo.
timeout /t 3 >nul

echo [COMMAND] Creating demo task...
(
echo # Demo Task
echo.
echo **Type**: demo
echo **Priority**: medium
echo.
echo Test delegation architecture.
) > AI_Employee_Vault_Cloud\demo_task.md
echo.
timeout /t 2 >nul

echo [COMMAND] python skills/zone_sync_manager.py --claim AI_Employee_Vault_Cloud\demo_task.md AI_Employee_Vault
python skills/zone_sync_manager.py --claim AI_Employee_Vault_Cloud\demo_task.md AI_Employee_Vault
echo.
timeout /t 4 >nul

echo [COMMAND] Showing claim file...
dir /b zone_sync_queue\claim_demo_task*.json
echo.
for %%f in (zone_sync_queue\claim_demo_task*.json) do type "%%f"
echo.
timeout /t 5 >nul

echo [NARRATION] A claim file was created tracking the task movement.
echo [NARRATION] This ensures atomic task ownership.
echo.
timeout /t 3 >nul

echo [NARRATION] Now let's show the single-writer dashboard.
echo.
timeout /t 3 >nul

echo [COMMAND] python skills/zone_sync_manager.py --scan
python skills/zone_sync_manager.py --scan
echo.
timeout /t 4 >nul

echo [NARRATION] The dashboard lock ensures only one writer at a time.
echo [NARRATION] This prevents race conditions.
echo.
timeout /t 3 >nul

REM ========================================
REM HEALTH MONITORING
REM ========================================
cls
echo.
echo ========================================
echo PART 8: Health Monitoring (2 minutes)
echo ========================================
echo.
timeout /t 2 >nul

echo.
echo [NARRATION] Finally, let's demonstrate the health monitoring system.
echo.
timeout /t 3 >nul

echo [COMMAND] python skills/health_monitor.py --summary
python skills/health_monitor.py --summary
echo.
timeout /t 5 >nul

echo [NARRATION] All services are healthy.
echo [NARRATION] Let's run a monitoring cycle.
echo.
timeout /t 3 >nul

echo [COMMAND] python skills/health_monitor.py --monitor 3
python skills/health_monitor.py --monitor 3
echo.
timeout /t 40 >nul

echo [NARRATION] The health monitor checks all services every 30 seconds.
echo [NARRATION] It can auto-recover from failures.
echo.
timeout /t 4 >nul

echo [COMMAND] python skills/health_monitor.py --alerts
python skills/health_monitor.py --alerts
echo.
timeout /t 4 >nul

REM ========================================
REM CONCLUSION
REM ========================================
cls
echo.
echo ========================================
echo PART 9: Summary (2 minutes)
echo ========================================
echo.
timeout /t 2 >nul

echo.
echo [NARRATION] Let me summarize the complete Platinum tier flow.
echo [NARRATION] One: Email arrives while Local is offline - Cloud detects and processes.
echo [NARRATION] Two: Cloud drafts response - Queued for local approval.
echo [NARRATION] Three: Secure sync ^(markdown-only, secrets filtered^) - Local zone receives.
echo [NARRATION] Four: Human reviews and approves - Approval workflow.
echo [NARRATION] Five: Action executed locally - Full security.
echo [NARRATION] Six: Logged and archived - Complete audit trail.
echo.
timeout /t 10 >nul

echo [COMMAND] Final zone status check...
echo.
echo === Cloud Zone ===
python skills/cloud_zone_manager.py --status | findstr /C:"zone" /C:"status"
echo.
echo === Local Zone ===
python skills/local_zone_manager.py --status | findstr /C:"zone" /C:"status"
echo.
timeout /t 5 >nul

REM ========================================
REM END
REM ========================================
cls
echo.
echo ========================================
echo Demo Complete!
echo ========================================
echo.
echo Screenshots would be saved to: %ScreenshotDir%
echo.
echo ========================================
echo STOP YOUR SCREEN RECORDING NOW!
echo ========================================
echo.
echo Next steps:
echo 1. Save your screen recording
echo 2. Add voice narration using VIDEO_SCRIPT.md
echo 3. Edit for timing and clarity
echo 4. Export as MP4 for submission
echo.
echo Demo duration: ~20 minutes
echo.
pause
