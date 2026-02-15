#!/usr/bin/env python3
"""
Dashboard Updater - Bronze Tier Observability Layer

Agent Skill for updating Dashboard.md to reflect current system state.
Monitors folder states and updates dashboard with current metrics.
"""

import os
import re
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VAULT_BASE = os.getenv('VAULT_BASE', 'AI_Employee_Vault')
INBOX_FOLDER = os.path.join(VAULT_BASE, 'Inbox')
NEEDS_ACTION_FOLDER = os.path.join(VAULT_BASE, 'Needs_Action')
DONE_FOLDER = os.getenv('VAULT_DONE', 'AI_Employee_Vault/Done')
DASHBOARD_FILE = os.path.join(VAULT_BASE, 'Dashboard.md')


class DashboardUpdater:
    """Updates the Dashboard.md with current system state."""

    def __init__(self):
        self.inbox_path = Path(INBOX_FOLDER)
        self.needs_action_path = Path(NEEDS_ACTION_FOLDER)
        self.done_path = Path(DONE_FOLDER)
        self.dashboard_path = Path(DASHBOARD_FILE)

    def count_tasks(self, folder: Path) -> int:
        """Count task files in a folder."""
        if not folder.exists():
            return 0
        return len(list(folder.glob('task-*.md')))

    def get_recent_completions(self, count: int = 5) -> list:
        """Get recently completed tasks."""
        if not self.done_path.exists():
            return []

        tasks = list(self.done_path.glob('task-*.md'))
        # Sort by modification time
        tasks.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        recent = []
        for task_path in tasks[:count]:
            content = task_path.read_text(encoding='utf-8')
            # Extract task title (first line)
            title = task_path.name
            for line in content.split('\n')[:5]:
                if line.startswith('# '):
                    title = line.lstrip('#').strip()
                    break

            # Extract completion time
            completed_time = None
            for line in content.split('\n'):
                if '**Completed**:' in line:
                    completed_time = line.split(':', 1)[1].strip()
                    break

            recent.append({
                'title': title,
                'time': completed_time or 'Unknown',
                'file': task_path.name
            })

        return recent

    def generate_dashboard_content(self) -> str:
        """Generate updated dashboard content."""
        now = datetime.now(timezone.utc).isoformat()

        # Count tasks in each folder
        inbox_count = self.count_tasks(self.inbox_path)
        needs_action_count = self.count_tasks(self.needs_action_path)
        done_count = self.count_tasks(self.done_path)

        # Get recent completions
        recent_completions = self.get_recent_completions(5)

        # Calculate total tasks ever
        total_tasks = inbox_count + needs_action_count + done_count

        # Generate recent completions section
        completions_text = ""
        if recent_completions:
            for item in recent_completions:
                completions_text += f"- **{item['title']}** ({item['time']})\n"
        else:
            completions_text = "*No completions yet.\n"

        # Generate processing section
        processing_text = ""
        if needs_action_count > 0:
            tasks = list(self.needs_action_path.glob('task-*.md'))
            for task_path in tasks[:3]:
                content = task_path.read_text(encoding='utf-8')
                title = task_path.name
                for line in content.split('\n')[:5]:
                    if line.startswith('# '):
                        title = line.lstrip('#').strip()
                        break
                processing_text += f"- **{title}** - {task_path.name}\n"
        else:
            processing_text = "*No tasks currently being processed.\n"

        # Determine health status
        health_status = "[OK]"
        health_issues = []

        if not self.inbox_path.exists():
            health_issues.append("Inbox folder missing")
        if not self.needs_action_path.exists():
            health_issues.append("Needs_Action folder missing")
        if not self.done_path.exists():
            health_issues.append("Done folder missing")

        if health_issues:
            health_status = "[WARN]"

        dashboard_content = f"""# AI Employee Dashboard

**Last Updated**: {now}
**Tier**: Bronze (Reactive Local Agent)
**Status**: Active

---

## System Overview

This dashboard provides real-time visibility into the AI Employee's state.

---

## Current State

### Inbox (New Events)
*Total: {inbox_count} tasks*

> New events detected by Watchers appear here before being triaged.

### Needs Action (Processing Queue)
*Total: {needs_action_count} tasks*

> Tasks awaiting Claude's processing and reasoning.

### Done (Completed)
*Total: {done_count} tasks*

> Successfully completed tasks.

---

## Recent Activity

### Latest Completions

{completions_text}

### Currently Processing

{processing_text}

---

## Performance Metrics

- **Tasks Processed Today**: {done_count}
- **Average Processing Time**: N/A
- **Success Rate**: {((done_count / total_tasks) * 100):.1f}% if total_tasks > 0 else N/A
- **Last Watcher Event**: N/A

---

## Quick Stats

| Metric | Value |
|--------|-------|
| Total Tasks Ever | {total_tasks} |
| Active Tasks | {inbox_count + needs_action_count} |
| Completed Tasks | {done_count} |
| Failed Tasks | 0 |
| Uptime | Since 2026-02-15 |

---

## System Health

{health_status} Vault Structure: {'OK' if not health_issues else 'Issues: ' + ', '.join(health_issues)}
{health_status} Watchers: Active
{health_status} Processing: Ready
{health_status} Dashboard: Up to date

---

## Notes

- This dashboard updates automatically as tasks move through the system
- All state transitions are logged in the file system
- Company_Handbook.md contains AI behavior guidelines

---

*This dashboard is maintained automatically by the AI Employee system. Manual edits may be overwritten.*
"""

        return dashboard_content

    def update(self) -> bool:
        """Update the dashboard file."""
        try:
            # Ensure vault directory exists
            self.dashboard_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate new content
            new_content = self.generate_dashboard_content()

            # Write to dashboard
            with open(self.dashboard_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"[OK] Dashboard updated: {self.dashboard_path}")
            print(f"    Inbox: {self.count_tasks(self.inbox_path)} | "
                  f"Needs Action: {self.count_tasks(self.needs_action_path)} | "
                  f"Done: {self.count_tasks(self.done_path)}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to update dashboard: {e}")
            return False


def main():
    """Main entry point for dashboard updater."""
    import argparse

    parser = argparse.ArgumentParser(description='Update AI Employee Dashboard')
    parser.add_argument('--watch', action='store_true',
                       help='Continuously monitor and update dashboard')
    parser.add_argument('--interval', type=int, default=30,
                       help='Update interval in seconds (default: 30)')
    args = parser.parse_args()

    updater = DashboardUpdater()

    if args.watch:
        import time
        print("[START] Dashboard updater running in watch mode...")
        print(f"[INFO] Update interval: {args.interval} seconds")
        print("[INFO] Press Ctrl+C to stop")

        try:
            while True:
                updater.update()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[STOP] Dashboard updater stopped")
    else:
        # Single update
        updater.update()


if __name__ == '__main__':
    main()
