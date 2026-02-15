@echo off
REM Platinum Tier Demo Test Script
REM Non-interactive version to test all demo commands

echo ========================================
echo Platinum Tier Demo Test
echo ========================================
echo.

REM Test 1: Check zone structures
echo [TEST 1] Checking Zone Structures...
echo.
if exist AI_Employee_Vault_Cloud (
    echo [OK] Cloud zone exists
    dir /b AI_Employee_Vault_Cloud
) else (
    echo [ERROR] Cloud zone missing
)
echo.

if exist AI_Employee_Vault (
    echo [OK] Local zone exists
    dir /b AI_Employee_Vault
) else (
    echo [ERROR] Local zone missing
)
echo.

if exist zone_sync_queue (
    echo [OK] Sync queue exists
) else (
    echo [ERROR] Sync queue missing
)
echo.

REM Test 2: Cloud zone status
echo [TEST 2] Cloud Zone Status...
echo.
python skills/cloud_zone_manager.py --status
if errorlevel 1 (
    echo [ERROR] Cloud zone manager failed
) else (
    echo [OK] Cloud zone manager working
)
echo.

REM Test 3: Local zone status
echo [TEST 3] Local Zone Status...
echo.
python skills/local_zone_manager.py --status
if errorlevel 1 (
    echo [ERROR] Local zone manager failed
) else (
    echo [OK] Local zone manager working
)
echo.

REM Test 4: Zone sync status
echo [TEST 4] Zone Sync Status...
echo.
python skills/zone_sync_manager.py --status
if errorlevel 1 (
    echo [ERROR] Zone sync manager failed
) else (
    echo [OK] Zone sync manager working
)
echo.

REM Test 5: Create test email task
echo [TEST 5] Creating Test Email Task...
echo.
if exist AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md (
    del AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md
)
(
echo # Task: Customer Inquiry about Q1 2026 Financial Reports
echo.
echo **Date**: 2026-02-15
echo **Type**: email-event
echo **Priority**: high
echo **Source**: cloud_zone ^(EmailWatcher^)
) > AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md

if exist AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md (
    echo [OK] Email task created
    type AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md
) else (
    echo [ERROR] Failed to create email task
)
echo.

REM Test 6: Triage task
echo [TEST 6] Triaging Task...
echo.
python skills/cloud_zone_manager.py --triage AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md
if errorlevel 1 (
    echo [ERROR] Triage failed
) else (
    echo [OK] Triage completed
    if exist AI_Employee_Vault_Cloud\Triage\triage_email_inquiry_q1_2026.json (
        echo [OK] Triage file created
        type AI_Employee_Vault_Cloud\Triage\triage_email_inquiry_q1_2026.json
    )
)
echo.

REM Test 7: Create draft
echo [TEST 7] Creating Draft in Cloud Zone...
echo.
python skills/cloud_zone_manager.py --draft linkedin "Test draft content for demo."
if errorlevel 1 (
    echo [ERROR] Draft creation failed
) else (
    echo [OK] Draft created
    dir /b AI_Employee_Vault_Cloud\Drafts
)
echo.

REM Test 8: Sync to local zone
echo [TEST 8] Syncing Task to Local Zone...
echo.
python skills/cloud_zone_manager.py --sync AI_Employee_Vault_Cloud\email_inquiry_q1_2026.md
if errorlevel 1 (
    echo [ERROR] Sync failed
) else (
    echo [OK] Sync completed
    if exist local_zone_sync\email_inquiry_q1_2026.md (
        echo [OK] Synced file exists
        type local_zone_sync\email_inquiry_q1_2026.md
    )
)
echo.

REM Test 9: Test secret filtering
echo [TEST 9] Testing Secret Filtering...
echo.
if exist AI_Employee_Vault_Cloud\secret_config.md (
    del AI_Employee_Vault_Cloud\secret_config.md
)
(
echo # Configuration
echo.
echo API_KEY = sk-1234567890abcdef
echo DATABASE_PASSWORD = mysecretpassword123
) > AI_Employee_Vault_Cloud\secret_config.md

python skills/zone_sync_manager.py --sync AI_Employee_Vault_Cloud\secret_config.md AI_Employee_Vault
echo [EXPECTED] Should see BLOCK message above
echo.

REM Test 10: Process in local zone
echo [TEST 10] Processing in Local Zone...
echo.
python skills/local_zone_manager.py --process local_zone_sync\email_inquiry_q1_2026.md
if errorlevel 1 (
    echo [ERROR] Process failed
) else (
    echo [OK] Process completed
    if exist AI_Employee_Vault\Pending_Approval (
        echo [OK] Approval request created
        dir /b AI_Employee_Vault\Pending_Approval
    )
)
echo.

REM Test 11: Approve action
echo [TEST 11] Approving Action...
echo.
for %%f in (AI_Employee_Vault\Pending_Approval\*.json) do (
    echo Processing approval: %%~nf
    python skills/local_zone_manager.py --approve %%~nf
    if errorlevel 1 (
        echo [ERROR] Approval failed for %%~nf
    ) else (
        echo [OK] Approved: %%~nf
    )
)
echo.

REM Test 12: Health check
echo [TEST 12] Health Summary...
echo.
python skills/health_monitor.py --summary
if errorlevel 1 (
    echo [ERROR] Health check failed
) else (
    echo [OK] Health check completed
)
echo.

REM Test 13: Final status
echo [TEST 13] Final Zone Status...
echo.
echo === Cloud Zone ===
python skills/cloud_zone_manager.py --status | findstr /C:"zone" /C:"status"
echo.
echo === Local Zone ===
python skills/local_zone_manager.py --status | findstr /C:"zone" /C:"status"
echo.

REM Summary
echo ========================================
echo Demo Test Complete!
echo ========================================
echo.
echo All critical demo commands tested successfully.
echo You can now run the full demo with screen recording.
echo.
echo To record demo:
echo 1. Start screen recording (Win+G or OBS)
echo 2. Run: record_demo.bat
echo 3. Follow prompts
echo 4. Stop recording when done
echo.
pause
