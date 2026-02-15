#!/bin/bash
# Scheduled Task Runner - Silver Tier Automation
# Cron-compatible script for Linux/Mac

echo "=========================================="
echo "AI Employee - Scheduled Task Runner"
echo "=========================================="
echo

# Activate virtual environment
source venv/bin/activate

# Run scheduled tasks
echo "[$(date)] Running scheduled tasks..."

# 1. Generate plans for complex tasks
echo "[1/4] Generating plans for complex tasks..."
python skills/plan_generator.py --all

# 2. Process pending tasks
echo "[2/4] Processing pending tasks..."
python skills/process_tasks.py --process

# 3. Update dashboard
echo "[3/4] Updating dashboard..."
python skills/update_dashboard.py

# 4. Check for approval requests
echo "[4/4] Checking approval requests..."
python skills/approval_workflow.py --stats

echo
echo "[$(date)] Scheduled tasks completed"
echo "=========================================="
echo
