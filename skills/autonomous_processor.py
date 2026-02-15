#!/usr/bin/env python3
"""
Autonomous Processor - Gold Tier Persistence

Implements Ralph Wiggum loop for continuous autonomous operation.
Monitors, processes, and recovers from failures with retry logic.

Requirements:
- python-dotenv: pip install python-dotenv
- time: Built-in
- json: Built-in
"""

import os
import json
import time
import shutil
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VAULT_BASE = Path(os.getenv('VAULT_BASE', 'AI_Employee_Vault'))
INBOX = VAULT_BASE / 'Inbox'
NEEDS_ACTION = VAULT_BASE / 'Needs_Action'
DONE = VAULT_BASE / 'Done'
AUDIT_LOG = Path('audit.log.jsonl')


class AutonomousProcessor:
    """Continuous autonomous task processing with persistence."""

    def __init__(self, max_retries=3, retry_delay=5):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.audit_log = AUDIT_LOG

    def log_action(self, action, status, details=None):
        """Log action to audit log."""
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'action': action,
            'status': status,
            'details': details or {}
        }

        with open(self.audit_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')

        return log_entry

    def move_with_retry(self, source, destination, action_name="move"):
        """Move file with retry logic."""
        attempt = 0

        while attempt < self.max_retries:
            try:
                shutil.move(str(source), str(destination))
                self.log_action(
                    action=f"{action_name}_file",
                    status="success",
                    details={
                        'source': str(source),
                        'destination': str(destination),
                        'attempts': attempt + 1
                    }
                )
                return True
            except Exception as e:
                attempt += 1
                if attempt >= self.max_retries:
                    self.log_action(
                        action=f"{action_name}_file",
                        status="failed",
                        details={
                            'source': str(source),
                            'error': str(e),
                            'attempts': attempt
                        }
                    )
                    return False
                time.sleep(self.retry_delay)

        return False

    def process_task(self, task_path):
        """Process a single task with full error handling."""
        try:
            # Read task
            content = task_path.read_text(encoding='utf-8')

            # Extract metadata
            task_type = "unknown"
            for line in content.split('\n')[:10]:
                if '**Type**:' in line:
                    task_type = line.split(':', 1)[1].strip()
                    break

            # Simulate processing (in production, would use TaskProcessor)
            print(f"[PROCESSING] {task_path.name} (type: {task_type})")

            # Move to Done with retry
            done_path = DONE / task_path.name

            # Add processing timestamp
            processed_content = content + f"\n\n## Autonomous Processing\n\n"
            processed_content += f"**Processed At**: {datetime.now(timezone.utc).isoformat()}\n"
            processed_content += f"**Processor**: Autonomous Loop\n"
            processed_content += f"**Retries**: 0\n"

            done_path.write_text(processed_content, encoding='utf-8')

            if self.move_with_retry(task_path, done_path, "process"):
                print(f"[OK] {task_path.name} processed")
                return True
            else:
                print(f"[FAILED] {task_path.name} - move failed")
                return False

        except Exception as e:
            self.log_action(
                action="process_task",
                status="error",
                details={
                    'task': str(task_path),
                    'error': str(e)
                }
            )
            print(f"[ERROR] Failed to process {task_path.name}: {e}")
            return False

    def detect_multi_step_tasks(self):
        """Detect tasks requiring multi-step completion."""
        multi_step = []

        for task_path in NEEDS_ACTION.glob('*.md'):
            content = task_path.read_text(encoding='utf-8')

            # Check for multi-step indicators
            step_indicators = ['and then', 'after that', 'next', 'finally', 'also']
            is_multi_step = any(indicator in content.lower() for indicator in step_indicators)

            if is_multi_step:
                multi_step.append(task_path)

        return multi_step

    def run_autonomous_loop(self, iterations=10):
        """Run Ralph Wiggum loop for continuous processing."""
        print("=" * 60)
        print("Autonomous Processor - Gold Tier Persistence")
        print("=" * 60)
        print()

        self.log_action(
            action="autonomous_loop_start",
            status="started",
            details={'iterations': iterations}
        )

        for i in range(iterations):
            print(f"\n[ITERATION {i+1}/{iterations}] {datetime.now().strftime('%H:%M:%S')}")

            # Step 1: Check Inbox for new tasks
            inbox_tasks = list(INBOX.glob('task-*.md'))
            print(f"[SCAN] Inbox: {len(inbox_tasks)} tasks")

            if inbox_tasks:
                for task in inbox_tasks:
                    # Move to Needs_Action first
                    needs_action_path = NEEDS_ACTION / task.name
                    if self.move_with_retry(task, needs_action_path, "inbox_to_processing"):
                        print(f"[MOVE] {task.name} → Needs_Action")

            # Step 2: Process tasks in Needs_Action
            needs_action_tasks = list(NEEDS_ACTION.glob('task-*.md'))
            print(f"[PROCESS] Needs_Action: {len(needs_action_tasks)} tasks")

            for task in needs_action_tasks:
                self.process_task(task)

            # Step 3: Detect multi-step tasks
            multi_step = self.detect_multi_step_tasks()
            if multi_step:
                print(f"[DETECT] {len(multi_step)} multi-step tasks found")

            # Step 4: Brief pause between iterations
            if i < iterations - 1:
                time.sleep(2)

        # Final summary
        print("\n" + "=" * 60)
        print("Autonomous Loop Complete")
        print("=" * 60)
        print()

        done_count = len(list(DONE.glob('task-*.md')))
        print(f"[SUMMARY] Total tasks completed: {done_count}")

        self.log_action(
            action="autonomous_loop_complete",
            status="completed",
            details={
                'iterations': iterations,
                'tasks_completed': done_count
            }
        )


def main():
    """Main entry point for autonomous processor."""
    import argparse

    parser = argparse.ArgumentParser(description='Run autonomous processing loop')
    parser.add_argument('--iterations', type=int, default=10,
                       help='Number of loop iterations (default: 10)')
    parser.add_argument('--watch', action='store_true',
                       help='Run in continuous watch mode')
    parser.add_argument('--audit', action='store_true',
                       help='View audit log')
    args = parser.parse_args()

    processor = AutonomousProcessor()

    if args.audit:
        print("\n=== AUDIT LOG ===")
        with open(processor.audit_log, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                print(f"{entry['timestamp']} | {entry['action']:20} | {entry['status']:10} | {entry.get('details', {})}")
        return

    if args.watch:
        print("[WATCH MODE] Running continuously (Ctrl+C to stop)")
        try:
            while True:
                processor.run_autonomous_loop(iterations=5)
                print("\n[WAIT] Pausing before next cycle...")
                time.sleep(30)
        except KeyboardInterrupt:
            print("\n[STOP] Watch mode stopped")
        return

    # Single run
    processor.run_autonomous_loop(iterations=args.iterations)


if __name__ == '__main__':
    main()
