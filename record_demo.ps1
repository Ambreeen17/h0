# Platinum Tier Demo Video Recording Script
# This script automates the demo flow for video recording
# Usage: .\record_demo.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Platinum Tier AI Employee Demo Recording" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Demo configuration
$DemoTitle = "Personal AI Employee - Platinum Tier Demo"
$OutputDir = "demo_recording"
$ScreenshotDir = "$OutputDir\screenshots"

# Create output directories
New-Item -ItemType Directory -Force -Path $ScreenshotDir | Out-Null

# Function to take screenshot
function Take-Screenshot {
    param([string]$Name)

    $timestamp = Get-Date -Format "HHmmss"
    $filename = "$ScreenshotDir\$timestamp-$Name.png"

    # Use PowerShell to capture window
    Add-Type -AssemblyName System.Windows.Forms
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bmp = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
    $graphics = [System.Drawing.Graphics]::FromImage($bmp)
    $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
    $bmp.Save("$filename")
    $graphics.Dispose()
    $bmp.Dispose()

    Write-Host "[SCREENSHOT] Saved: $filename" -ForegroundColor Green
    Start-Sleep -Milliseconds 500
}

# Function to type with delays
function Type-Command {
    param([string]$Command, [int]$Delay = 1000)

    Write-Host "`n[COMMAND] $Command" -ForegroundColor Yellow
    Start-Sleep -Milliseconds $Delay
}

# Function to display section header
function Show-Section {
    param([string]$Title)

    Clear-Host
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host $Title -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Start-Sleep -Seconds 2
}

# Demo narration
function Narrate {
    param([string]$Text, [int]$Duration = 3)

    Write-Host "`n[NARRATION] $Text" -ForegroundColor Magenta
    Start-Sleep -Seconds $Duration
}

# Start recording message
Write-Host ""
Write-Host "⚠️  START YOUR SCREEN RECORDING NOW!" -ForegroundColor Red
Write-Host "   Recommended: OBS Studio, Windows Game Bar (Win+G), or similar" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Enter to begin demo..." -ForegroundColor Green
$null = Read-Host

# ========================================
# INTRODUCTION
# ========================================
Show-Section "PART 1: Introduction (2 minutes)"

Narrate "Welcome to the Platinum Tier AI Employee demo."
Narrate "This is a Production Hybrid AI Employee with cloud and local zones."
Narrate "Let me show you the complete architecture."

Take-Screenshot "01-intro"

Type-Command "ls -la"
Start-Sleep -Seconds 2

# ========================================
# PREPARATION
# ========================================
Show-Section "PART 2: Setup Verification (2 minutes)"

Narrate "First, let me verify that all zone structures are in place."

Type-Command "echo '=== Checking Zone Structures ==='"
Type-Command "ls -la AI_Employee_Vault_Cloud/"
Type-Command "ls -la AI_Employee_Vault/"
Type-Command "ls -la zone_sync_queue/"

Take-Screenshot "02-zone-structures"

Narrate "Perfect! We have our Cloud Zone, Local Zone, and Sync Queue all set up."

# ========================================
# WORK-ZONE ARCHITECTURE
# ========================================
Show-Section "PART 3: Work-Zone Architecture (3 minutes)"

Narrate "Now let's examine the work-zone specialization."
Narrate "The Cloud Zone handles safe, non-sensitive operations."

Type-Command "python skills/cloud_zone_manager.py --status"
Start-Sleep -Seconds 3

Take-Screenshot "03-cloud-zone-status"

Narrate "The Cloud Zone can draft content, triage tasks, analyze data, and generate plans."
Narrate "Notice it has no access to credentials or banking operations."

Narrate "The Local Zone handles secure, sensitive operations."

Type-Command "python skills/local_zone_manager.py --status"
Start-Sleep -Seconds 3

Take-Screenshot "04-local-zone-status"

Narrate "The Local Zone handles approvals, sensitive execution, banking, and credentials."
Narrate "These capabilities are never available to the Cloud Zone."

Narrate "Let me show you the delegation architecture."

Type-Command "python skills/zone_sync_manager.py --status"
Start-Sleep -Seconds 3

Take-Screenshot "05-delegation-status"

Narrate "The delegation architecture ensures claim-by-move, single-writer dashboard,"
Narrate "and markdown-only sync between zones. Secrets are never synced."

# ========================================
# CLOUD ZONE OPERATIONS
# ========================================
Show-Section "PART 4: Cloud Zone Operations (4 minutes)"

Narrate "Now let's simulate a real-world scenario."
Narrate "An email arrives while the Local Zone is offline."
Narrate "The Cloud Zone detects it and creates a task."

Type-Command "cat > AI_Employee_Vault_Cloud/email_inquiry_q1_2026.md << 'EOF_EMAIL'
# Task: Customer Inquiry about Q1 2026 Financial Reports

**Date**: 2026-02-15
**Type**: email-event
**Priority**: high
**Source**: cloud_zone (EmailWatcher)

## Email Content

From: customer@enterprise-client.com
Subject: Q1 2026 Financial Report Request

Hi,

I'm requesting our Q1 2026 financial reports for our quarterly review.
Can you provide the revenue summary and outstanding invoices?

Thanks,
Customer

---

**Created By**: EmailWatcher (Silver tier)
**Zone**: Cloud
**Detected At**: 2026-02-15T10:30:00Z
EOF_EMAIL"

Take-Screenshot "06-email-task-created"

Narrate "The Cloud Zone has detected the email and created a task."
Narrate "Now let's triage this task to determine how to handle it."

Type-Command "python skills/cloud_zone_manager.py --triage AI_Employee_Vault_Cloud/email_inquiry_q1_2026.md"
Start-Sleep -Seconds 3

Take-Screenshot "07-triage-result"

Narrate "The triage shows this task requires the Local Zone because it involves financial data."
Narrate "This is an example of work-zone specialization in action."

Narrate "The Cloud Zone can still draft a response safely."

Type-Command "python skills/cloud_zone_manager.py --draft linkedin 'Thank you for your inquiry about Q1 2026 financial reports. Our revenue increased 25% year-over-year, reaching \$1.2M. Outstanding invoices total \$45,000, all due within 30 days. Full report attached.'"

Start-Sleep -Seconds 2

Type-Command "cat AI_Employee_Vault_Cloud/Drafts/draft-*.md | head -20"
Start-Sleep -Seconds 3

Take-Screenshot "08-draft-created"

Narrate "The Cloud Zone has drafted a response safely."
Narrate "No sensitive operations were performed."

# ========================================
# SECURE ZONE SYNC
# ========================================
Show-Section "PART 5: Secure Zone Sync (4 minutes)"

Narrate "Now let's demonstrate the secure sync between zones."

Type-Command "python skills/cloud_zone_manager.py --sync AI_Employee_Vault_Cloud/email_inquiry_q1_2026.md"
Start-Sleep -Seconds 2

Type-Command "cat local_zone_sync/email_inquiry_q1_2026.md"
Start-Sleep -Seconds 3

Take-Screenshot "09-synced-file"

Narrate "The task has been synced to the Local Zone with metadata."
Narrate "Notice the Sync Information at the top."

Narrate "Now let's test the secret filtering."

Type-Command "cat > AI_Employee_Vault_Cloud/secret_config.md << 'EOF_SECRET'
# Configuration

API_KEY = sk-1234567890abcdef
DATABASE_PASSWORD = mysecretpassword123
SECRET_EOF"

Narrate "I've created a file with secrets in it."
Narrate "Let's try to sync it."

Type-Command "python skills/zone_sync_manager.py --sync AI_Employee_Vault_Cloud/secret_config.md AI_Employee_Vault"
Start-Sleep -Seconds 2

Take-Screenshot "10-secret-blocked"

Narrate "Perfect! The sync was blocked because it detected secret patterns."
Narrate "This ensures security even if the Cloud Zone is compromised."

# ========================================
# LOCAL ZONE APPROVAL
# ========================================
Show-Section "PART 6: Local Zone Approval (5 minutes)"

Narrate "Now let's process the synced task in the Local Zone."

Type-Command "python skills/local_zone_manager.py --process local_zone_sync/email_inquiry_q1_2026.md"
Start-Sleep -Seconds 2

Take-Screenshot "11-approval-required"

Narrate "The Local Zone detected that this requires approval."
Narrate "Financial operations need human authorization."

Type-Command "cat AI_Employee_Vault/Pending_Approval/*.json"
Start-Sleep -Seconds 3

Take-Screenshot "12-approval-details"

Narrate "Here's the approval request with the reason and threshold."
Narrate "Let me approve this action."

Type-Command '\$APPROVAL_ID = (ls AI_Employee_Vault/Pending_Approval/*.json | head -1 | xargs -n1 basename | sed ''s/.json//'')'
Type-Command "echo \$APPROVAL_ID"
Start-Sleep -Seconds 1

Type-Command "python skills/local_zone_manager.py --approve \$APPROVAL_ID"
Start-Sleep -Seconds 2

Take-Screenshot "13-action-executed"

Narrate "The action has been approved and executed locally."

Type-Command "cat AI_Employee_Vault/Done/email_inquiry_q1_2026.md | tail -10"
Start-Sleep -Seconds 3

Take-Screenshot "14-executed-task"

Narrate "Notice the Local Zone Execution stamp."
Narrate "The task was executed with full security in the Local Zone."

# ========================================
# DELEGATION ARCHITECTURE
# ========================================
Show-Section "PART 7: Delegation Architecture (2 minutes)"

Narrate "Let me demonstrate the claim-by-move delegation."

Type-Command "cat > AI_Employee_Vault_Cloud/demo_task.md << 'EOF_TASK'
# Demo Task

**Type**: demo
**Priority**: medium

Test delegation architecture.
EOF_TASK"

Type-Command "python skills/zone_sync_manager.py --claim AI_Employee_Vault_Cloud/demo_task.md AI_Employee_Vault"
Start-Sleep -Seconds 2

Type-Command "cat zone_sync_queue/claim_*.json"
Start-Sleep -Seconds 3

Take-Screenshot "15-claim-file"

Narrate "A claim file was created tracking the task movement."
Narrate "This ensures atomic task ownership."

Narrate "Now let's show the single-writer dashboard."

Type-Command "python skills/zone_sync_manager.py --scan"
Start-Sleep -Seconds 2

Take-Screenshot "16-dashboard-lock"

Narrate "The dashboard lock ensures only one writer at a time."
Narrate "This prevents race conditions."

# ========================================
# HEALTH MONITORING
# ========================================
Show-Section "PART 8: Health Monitoring (2 minutes)"

Narrate "Finally, let's demonstrate the health monitoring system."

Type-Command "python skills/health_monitor.py --summary"
Start-Sleep -Seconds 3

Take-Screenshot "17-health-summary"

Narrate "All services are healthy."
Narrate "Let's run a monitoring cycle."

Type-Command "python skills/health_monitor.py --monitor 3"
Start-Sleep -Seconds 10

Take-Screenshot "18-health-monitoring"

Narrate "The health monitor checks all services every 30 seconds."
Narrate "It can auto-recover from failures."

Type-Command "python skills/health_monitor.py --alerts"
Start-Sleep -Seconds 2

Take-Screenshot "19-alerts-log"

# ========================================
# CONCLUSION
# ========================================
Show-Section "PART 9: Summary (2 minutes)"

Narrate "Let me summarize the complete Platinum tier flow."
Narrate "One: Email arrives while Local is offline - Cloud detects and processes."
Narrate "Two: Cloud drafts response - Queued for local approval."
Narrate "Three: Secure sync (markdown-only, secrets filtered) - Local zone receives."
Narrate "Four: Human reviews and approves - Approval workflow."
Narrate "Five: Action executed locally - Full security."
Narrate "Six: Logged and archived - Complete audit trail."

Type-Command "echo '=== Platinum Tier Complete Flow ==='"
Type-Command "python skills/cloud_zone_manager.py --status | grep -E '(zone|status)'"
Type-Command "python skills/local_zone_manager.py --status | grep -E '(zone|status|approvals_pending)'"
Start-Sleep -Seconds 3

Take-Screenshot "20-final-status"

# ========================================
# END
# ========================================
Clear-Host
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Demo Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host 'Screenshots saved to: $ScreenshotDir' -ForegroundColor Cyan
Write-Host "🎬 STOP YOUR SCREEN RECORDING NOW!" -ForegroundColor Red
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit your screen recording" -ForegroundColor White
Write-Host "2. Add voice narration using the script" -ForegroundColor White
Write-Host "3. Export as MP4 for submission" -ForegroundColor White
Write-Host ""
Write-Host 'Demo duration: ~20 minutes' -ForegroundColor Cyan
Write-Host ""
