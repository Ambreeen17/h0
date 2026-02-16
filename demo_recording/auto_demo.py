#!/usr/bin/env python3
"""
Automated Demo Activity Generator
Creates tasks and moves them through the workflow for recording
"""

import os
import time
import shutil
from pathlib import Path
from datetime import datetime, timezone

# Paths
VAULT_BASE = Path('AI_Employee_Vault')
VAULT_CLOUD = Path('AI_Employee_Vault_CLOUD')
NEEDS_ACTION = VAULT_BASE / 'Needs_Action'
DONE = VAULT_BASE / 'Done'

def create_task(title, task_type, priority, content):
    """Create a new task in Needs_Action"""
    timestamp = datetime.now(timezone.utc).isoformat()
    task_id = timestamp.replace(':', '-').replace('.', '-')[:19]

    task_content = f"""# {title}

**Date**: {timestamp}
**Type**: {task_type}
**Priority**: {priority}
**Source**: demo_recording

## Description

{content}

---

**Created By**: Demo Automation
**Zone**: Local
"""

    task_file = NEEDS_ACTION / f"task-{task_id}.md"
    task_file.write_text(task_content, encoding='utf-8')
    print(f"[TASK CREATED] {title}")
    return task_file

def complete_task(task_file):
    """Move task to Done"""
    done_file = DONE / task_file.name

    # Add completion stamp
    content = task_file.read_text(encoding='utf-8')
    content += f"""

## Completed

**Completed At**: {datetime.now(timezone.utc).isoformat()}
**Status**: ✅ Complete
**Processed By**: Demo Automation
"""

    done_file.write_text(content, encoding='utf-8')
    shutil.move(str(task_file), str(done_file))
    print(f"[TASK COMPLETED] {task_file.stem}")

print("=" * 60)
print("AI EMPLOYEE DEMO - AUTOMATED ACTIVITY")
print("=" * 60)
print()

# Scenario 1: Customer Support
print("\n[SCENE 1] Customer support request arrives...")
task1 = create_task(
    "Customer: Refund Request",
    "user-request",
    "high",
    "Customer asking about refund for Order #12345. Needs review and approval."
)
time.sleep(2)

# Scenario 2: Financial Report
print("\n[SCENE 2] Financial report generation needed...")
task2 = create_task(
    "Generate Weekly Financial Report",
    "financial-task",
    "high",
    "Prepare Q1 financial summary for CEO review. Requires approval before sending."
)
time.sleep(2)

# Scenario 3: Email Inquiry
print("\n[SCENE 3] Email inquiry received...")
task3 = create_task(
    "Partner: Integration Question",
    "email-event",
    "medium",
    "Technical partner asking about API integration. Draft response needed."
)
time.sleep(2)

print("\n" + "=" * 60)
print("TASKS CREATED - WATCH DASHBOARD UPDATE!")
print("=" * 60)
print()
print("Dashboard should show 3 new tasks in 'Needs Action'")
print("Waiting 5 seconds for auto-refresh...")
print()
time.sleep(5)

# Complete first task
print("\n[SCENE 4] Processing first task...")
complete_task(task1)
print("Task moved to Done - Dashboard updating!")
time.sleep(3)

# Complete second task
print("\n[SCENE 5] Processing second task...")
complete_task(task2)
print("Another task completed!")
time.sleep(3)

print("\n" + "=" * 60)
print("DEMO COMPLETE!")
print("=" * 60)
print()
print("Check dashboard for:")
print("  - Tasks moved to 'Done' section")
print("  - Updated metrics (tasks completed increased)")
print("  - Activity feed showing completions")
print()
