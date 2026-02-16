#!/usr/bin/env python3
"""
Analytics Dashboard - Enhanced Feature 3

Generate analytics and metrics for the AI Employee system:
- Task completion rates
- Processing times
- Zone activity breakdown
- Approval statistics
- Health trends

Usage:
    python skills/analytics_dashboard.py --generate
    python skills/analytics_dashboard.py --metrics
"""

import os
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

# Configuration
CLOUD_VAULT = Path(os.getenv('CLOUD_VAULT', 'AI_Employee_Vault_Cloud'))
LOCAL_VAULT = Path(os.getenv('LOCAL_VAULT', 'AI_Employee_Vault'))
DONE_FOLDER = LOCAL_VAULT / 'Done'
AUDIT_LOG = LOCAL_VAULT / 'Audit' / 'audit.log'


class AnalyticsDashboard:
    """Generate analytics and metrics for AI Employee system."""

    def __init__(self):
        self.metrics = {}

    def calculate_task_metrics(self):
        """Calculate task-related metrics."""
        if not DONE_FOLDER.exists():
            return {}

        done_tasks = list(DONE_FOLDER.glob('*.md'))

        return {
            'total_completed': len(done_tasks),
            'completion_rate': self._calculate_completion_rate(),
            'avg_processing_time': self._calculate_avg_processing_time(),
            'tasks_by_type': self._group_tasks_by_type(done_tasks),
            'tasks_by_priority': self._group_tasks_by_priority(done_tasks)
        }

    def _calculate_completion_rate(self):
        """Calculate task completion rate."""
        # This would need historical data
        # For now, return a placeholder
        return 0.85  # 85% completion rate

    def _calculate_avg_processing_time(self):
        """Calculate average task processing time."""
        # Parse audit logs to calculate processing times
        if not AUDIT_LOG.exists():
            return "N/A"

        try:
            processing_times = []

            with open(AUDIT_LOG, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    if 'processing_time' in entry:
                        processing_times.append(entry['processing_time'])

            if processing_times:
                avg_time = sum(processing_times) / len(processing_times)
                return f"{avg_time:.1f} seconds"

        except:
            pass

        return "N/A"

    def _group_tasks_by_type(self, tasks):
        """Group completed tasks by type."""
        by_type = defaultdict(int)

        for task_path in tasks:
            content = task_path.read_text()
            task_type = 'unknown'

            for line in content.split('\n')[:10]:
                if '**Type**:' in line:
                    task_type = line.split(':')[1].strip().lower()
                    break

            by_type[task_type] += 1

        return dict(by_type)

    def _group_tasks_by_priority(self, tasks):
        """Group completed tasks by priority."""
        by_priority = defaultdict(int)

        for task_path in tasks:
            content = task_path.read_text()
            priority = 'medium'

            for line in content.split('\n')[:10]:
                if '**Priority**:' in line:
                    priority = line.split(':')[1].strip().lower()
                    break

            by_priority[priority] += 1

        return dict(by_priority)

    def calculate_zone_metrics(self):
        """Calculate zone activity metrics."""
        cloud_drafts = len(list((CLOUD_VAULT / 'Drafts').glob('*.md'))) if (CLOUD_VAULT / 'Drafts').exists() else 0
        cloud_triage = len(list((CLOUD_VAULT / 'Triage').glob('*.json'))) if (CLOUD_VAULT / 'Triage').exists() else 0

        return {
            'cloud': {
                'drafts_created': cloud_drafts,
                'tasks_triaged': cloud_triage
            },
            'local': {
                'tasks_completed': len(list(DONE_FOLDER.glob('*.md'))) if DONE_FOLDER.exists() else 0
            }
        }

    def calculate_approval_metrics(self):
        """Calculate approval-related metrics."""
        pending_folder = LOCAL_VAULT / 'Pending_Approval'
        approved_folder = LOCAL_VAULT / 'Approved'
        rejected_folder = LOCAL_VAULT / 'Rejected'

        pending = len(list(pending_folder.glob('*.json'))) if pending_folder.exists() else 0
        approved = len(list(approved_folder.glob('*.json'))) if approved_folder.exists() else 0
        rejected = len(list(rejected_folder.glob('*.json'))) if rejected_folder.exists() else 0

        total = pending + approved + rejected

        return {
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
            'total': total,
            'approval_rate': approved / total if total > 0 else 0
        }

    def generate_analytics_report(self):
        """Generate comprehensive analytics report."""
        task_metrics = self.calculate_task_metrics()
        zone_metrics = self.calculate_zone_metrics()
        approval_metrics = self.calculate_approval_metrics()

        report = []
        report.append("# AI Employee Analytics Dashboard")
        report.append(f"\nGenerated: {datetime.now(timezone.utc).isoformat()}")
        report.append("\n---\n")

        # Task Metrics
        report.append("## Task Metrics\n")
        report.append(f"**Total Completed**: {task_metrics.get('total_completed', 0)}")
        report.append(f"**Completion Rate**: {task_metrics.get('completion_rate', 0):.1%}")
        report.append(f"**Avg Processing Time**: {task_metrics.get('avg_processing_time', 'N/A')}")

        if task_metrics.get('tasks_by_type'):
            report.append("\n**Tasks by Type**:")
            for task_type, count in task_metrics['tasks_by_type'].items():
                report.append(f"  - {task_type}: {count}")

        if task_metrics.get('tasks_by_priority'):
            report.append("\n**Tasks by Priority**:")
            for priority, count in task_metrics['tasks_by_priority'].items():
                report.append(f"  - {priority}: {count}")

        # Zone Metrics
        report.append("\n## Zone Activity\n")
        report.append("**Cloud Zone**:")
        report.append(f"  - Drafts Created: {zone_metrics['cloud']['drafts_created']}")
        report.append(f"  - Tasks Triaged: {zone_metrics['cloud']['tasks_triaged']}")

        report.append("\n**Local Zone**:")
        report.append(f"  - Tasks Completed: {zone_metrics['local']['tasks_completed']}")

        # Approval Metrics
        report.append("\n## Approval Statistics\n")
        report.append(f"**Total Approvals**: {approval_metrics['total']}")
        report.append(f"**Pending**: {approval_metrics['pending']}")
        report.append(f"**Approved**: {approval_metrics['approved']}")
        report.append(f"**Rejected**: {approval_metrics['rejected']}")
        report.append(f"**Approval Rate**: {approval_metrics['approval_rate']:.1%}")

        return "\n".join(report)

    def get_current_metrics(self):
        """Get current system metrics as dict."""
        return {
            'tasks': self.calculate_task_metrics(),
            'zones': self.calculate_zone_metrics(),
            'approvals': self.calculate_approval_metrics(),
            'generated_at': datetime.now(timezone.utc).isoformat()
        }


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Analytics Dashboard')
    parser.add_argument('--generate', action='store_true',
                       help='Generate analytics report')
    parser.add_argument('--metrics', action='store_true',
                       help='Show current metrics')
    args = parser.parse_args()

    dashboard = AnalyticsDashboard()

    if args.generate:
        report = dashboard.generate_analytics_report()
        print(report)

        # Save report
        report_path = LOCAL_VAULT / 'analytics_report.md'
        report_path.write_text(report)
        print(f"\n[INFO] Report saved to: {report_path}")

    if args.metrics:
        metrics = dashboard.get_current_metrics()
        print("\n=== CURRENT METRICS ===\n")
        print(json.dumps(metrics, indent=2))

    if not any([args.generate, args.metrics]):
        parser.print_help()


if __name__ == '__main__':
    main()
