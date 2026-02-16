#!/usr/bin/env python3
"""
Task Prioritizer - Enhanced Feature 1

Intelligent task prioritization algorithm that considers:
- Task type and complexity
- Deadline proximity
- Resource requirements
- Dependencies
- Business impact

Usage:
    python skills/task_prioritizer.py --prioritize
    python skills/task_prioritizer.py --score path/to/task.md
"""

import os
import json
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# Configuration
NEEDS_ACTION = Path(os.getenv('LOCAL_VAULT', 'AI_Employee_Vault')) / 'Needs_Action'


class TaskPrioritizer:
    """Intelligent task prioritization system."""

    def __init__(self):
        self.priority_weights = {
            'deadline': 0.35,      # Deadline proximity
            'impact': 0.25,        # Business impact
            'complexity': 0.20,    # Task complexity
            'resources': 0.10,     # Resource availability
            'dependencies': 0.10   # Dependency blocking
        }

    def calculate_priority_score(self, task_path):
        """
        Calculate priority score for a task.

        Returns: float (0.0 - 1.0, higher = more urgent)
        """
        content = task_path.read_text()

        # Extract metadata
        metadata = self._extract_metadata(content)

        # Calculate component scores
        deadline_score = self._score_deadline(metadata)
        impact_score = self._score_impact(metadata)
        complexity_score = self._score_complexity(metadata)
        resource_score = self._score_resources(metadata)
        dependency_score = self._score_dependencies(metadata)

        # Weighted sum
        total_score = (
            deadline_score * self.priority_weights['deadline'] +
            impact_score * self.priority_weights['impact'] +
            complexity_score * self.priority_weights['complexity'] +
            resource_score * self.priority_weights['resources'] +
            dependency_score * self.priority_weights['dependencies']
        )

        return round(total_score, 3), {
            'deadline': deadline_score,
            'impact': impact_score,
            'complexity': complexity_score,
            'resources': resource_score,
            'dependencies': dependency_score
        }

    def _extract_metadata(self, content):
        """Extract metadata from task content."""
        metadata = {
            'priority': 'medium',
            'type': 'unknown',
            'deadline': None,
            'impact': 'medium',
            'estimated_hours': None,
            'dependencies': []
        }

        for line in content.split('\n'):
            if '**Priority**:' in line:
                metadata['priority'] = line.split(':')[1].strip().lower()
            elif '**Type**:' in line:
                metadata['type'] = line.split(':')[1].strip().lower()
            elif '**Deadline**:' in line:
                metadata['deadline'] = line.split(':')[1].strip()
            elif '**Impact**:' in line:
                metadata['impact'] = line.split(':')[1].strip().lower()
            elif '**Estimated**:' in line:
                hours = line.split(':')[1].strip()
                try:
                    metadata['estimated_hours'] = float(hours.replace('hours', '').strip())
                except:
                    pass
            elif '**Depends**:' in line:
                deps = line.split(':')[1].strip()
                metadata['dependencies'] = [d.strip() for d in deps.split(',')]

        return metadata

    def _score_deadline(self, metadata):
        """Score based on deadline proximity (0-1)."""
        if not metadata['deadline']:
            return 0.3  # Default: moderate urgency

        try:
            deadline = datetime.fromisoformat(metadata['deadline'])
            days_until = (deadline - datetime.now(timezone.utc)).days

            if days_until < 0:
                return 1.0  # Overdue
            elif days_until <= 1:
                return 0.9  # Due today/tomorrow
            elif days_until <= 3:
                return 0.7  # Due within 3 days
            elif days_until <= 7:
                return 0.5  # Due within a week
            elif days_until <= 14:
                return 0.3  # Due within 2 weeks
            else:
                return 0.1  # Plenty of time
        except:
            return 0.3

    def _score_impact(self, metadata):
        """Score based on business impact (0-1)."""
        impact = metadata.get('impact', 'medium')

        impact_scores = {
            'critical': 1.0,
            'high': 0.8,
            'medium': 0.5,
            'low': 0.2,
            'minimal': 0.0
        }

        return impact_scores.get(impact, 0.5)

    def _score_complexity(self, metadata):
        """Score based on task complexity (0-1, higher = simpler)."""
        # Simpler tasks get higher priority (quick wins)
        task_type = metadata.get('type', 'unknown')
        hours = metadata.get('estimated_hours', 4)

        # Type complexity
        type_complexity = {
            'draft': 0.8,
            'review': 0.9,
            'email-event': 0.7,
            'user-request': 0.5,
            'watcher-event': 0.6,
            'financial': 0.4,
            'complex-project': 0.2
        }

        base_score = type_complexity.get(task_type, 0.5)

        # Adjust by estimated hours
        if hours:
            if hours <= 1:
                hour_multiplier = 1.0
            elif hours <= 4:
                hour_multiplier = 0.8
            elif hours <= 8:
                hour_multiplier = 0.6
            else:
                hour_multiplier = 0.4

            return base_score * hour_multiplier

        return base_score

    def _score_resources(self, metadata):
        """Score based on resource availability (0-1)."""
        # For now, return neutral score
        # TODO: Integrate with resource management system
        return 0.5

    def _score_dependencies(self, metadata):
        """Score based on dependency blocking (0-1)."""
        deps = metadata.get('dependencies', [])

        if not deps:
            return 0.5  # No dependencies

        # Check if dependencies are complete
        done_folder = Path(os.getenv('LOCAL_VAULT', 'AI_Employee_Vault')) / 'Done'

        complete_count = sum(1 for dep in deps if (done_folder / f"{dep}.md").exists())

        if complete_count == len(deps):
            return 0.9  # All dependencies met
        elif complete_count > 0:
            return 0.4  # Some dependencies met
        else:
            return 0.1  # Blocked by dependencies

    def prioritize_all_tasks(self):
        """Prioritize all tasks in Needs_Action folder."""
        if not NEEDS_ACTION.exists():
            print(f"[INFO] No Needs_Action folder found")
            return []

        tasks = list(NEEDS_ACTION.glob('*.md'))
        if not tasks:
            print(f"[INFO] No tasks to prioritize")
            return []

        prioritized = []

        for task_path in tasks:
            score, components = self.calculate_priority_score(task_path)
            prioritized.append({
                'task': task_path.name,
                'score': score,
                'components': components
            })

        # Sort by score (descending)
        prioritized.sort(key=lambda x: x['score'], reverse=True)

        return prioritized

    def generate_priority_report(self):
        """Generate priority report for all tasks."""
        tasks = self.prioritize_all_tasks()

        if not tasks:
            return None

        report = []
        report.append("# Task Priority Report")
        report.append(f"\nGenerated: {datetime.now(timezone.utc).isoformat()}")
        report.append(f"\nTotal Tasks: {len(tasks)}")
        report.append("\n## Prioritized Tasks\n")

        for i, task in enumerate(tasks, 1):
            report.append(f"### {i}. {task['task']}")
            report.append(f"**Priority Score**: {task['score']:.2f}")
            report.append(f"\n**Components**:")
            for component, score in task['components'].items():
                report.append(f"  - {component}: {score:.2f}")
            report.append("")

        return "\n".join(report)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Task Prioritizer')
    parser.add_argument('--prioritize', action='store_true',
                       help='Prioritize all tasks')
    parser.add_argument('--score', metavar='TASK_FILE',
                       help='Calculate priority score for specific task')
    parser.add_argument('--report', action='store_true',
                       help='Generate priority report')
    args = parser.parse_args()

    prioritizer = TaskPrioritizer()

    if args.prioritize:
        tasks = prioritizer.prioritize_all_tasks()

        print("\n=== TASK PRIORITY ===\n")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task['task']} - Score: {task['score']:.2f}")

    if args.score:
        task_path = Path(args.score)
        if task_path.exists():
            score, components = prioritizer.calculate_priority_score(task_path)
            print(f"\n=== PRIORITY SCORE: {task_path.name} ===")
            print(f"Total Score: {score:.2f}")
            print("\nComponents:")
            for component, value in components.items():
                print(f"  {component}: {value:.2f}")
        else:
            print(f"[ERROR] Task not found: {args.score}")

    if args.report:
        report = prioritizer.generate_priority_report()
        if report:
            print(report)

            # Save report
            report_path = NEEDS_ACTION.parent / 'priority_report.md'
            report_path.write_text(report)
            print(f"\n[INFO] Report saved to: {report_path}")
        else:
            print("[INFO] No tasks to report on")

    if not any([args.prioritize, args.score, args.report]):
        parser.print_help()


if __name__ == '__main__':
    main()
