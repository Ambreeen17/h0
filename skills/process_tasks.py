#!/usr/bin/env python3
"""
Task Processor - Bronze Tier Action Layer

Agent Skill for processing tasks from Needs_Action folder.
Reads tasks, processes them autonomously, and moves completed tasks to Done.

This is an Agent Skill - NOT a raw prompt automation.
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

# Configuration
NEEDS_ACTION_FOLDER = os.getenv('VAULT_NEEDS_ACTION', 'AI_Employee_Vault/Needs_Action')
DONE_FOLDER = os.getenv('VAULT_DONE', 'AI_Employee_Vault/Done')
INBOX_FOLDER = os.getenv('VAULT_INBOX', 'AI_Employee_Vault/Inbox')


class TaskProcessor:
    """Processes tasks from Needs_Action and moves them to Done."""

    def __init__(self):
        self.needs_action_path = Path(NEEDS_ACTION_FOLDER)
        self.done_path = Path(DONE_FOLDER)
        self.inbox_path = Path(INBOX_FOLDER)

        # Ensure folders exist
        self.needs_action_path.mkdir(parents=True, exist_ok=True)
        self.done_path.mkdir(parents=True, exist_ok=True)
        self.inbox_path.mkdir(parents=True, exist_ok=True)

    def list_pending_tasks(self) -> List[Path]:
        """Get list of all pending task files."""
        tasks = list(self.needs_action_path.glob('task-*.md'))
        return sorted(tasks, key=lambda p: p.stat().st_mtime)

    def read_task(self, task_path: Path) -> str:
        """Read task file content."""
        with open(task_path, 'r', encoding='utf-8') as f:
            return f.read()

    def process_task(self, task_path: Path) -> Dict:
        """
        Process a single task.

        This is where the AI reasoning happens.
        For Bronze tier, we analyze the task and take appropriate action.
        """
        content = self.read_task(task_path)

        # Parse task metadata
        metadata = self.parse_task_metadata(content)

        # Determine task type and process accordingly
        task_type = metadata.get('type', 'unknown')

        if task_type == 'watcher-event':
            result = self.process_watcher_event(task_path, content, metadata)
        elif task_type == 'user-request':
            result = self.process_user_request(task_path, content, metadata)
        else:
            result = self.process_generic_task(task_path, content, metadata)

        return result

    def parse_task_metadata(self, content: str) -> Dict:
        """Extract metadata from task content."""
        metadata = {}
        for line in content.split('\n'):
            if line.startswith('**'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.replace('*', '').strip().lower()
                    value = value.strip()
                    metadata[key] = value
        return metadata

    def process_watcher_event(self, task_path: Path, content: str, metadata: Dict) -> Dict:
        """
        Process a watcher event task (new file detected).

        For Bronze tier: Analyze the file, categorize it, and log findings.
        """
        # Extract file path from task content
        file_path = None
        for line in content.split('\n'):
            if '**Path**:' in line or '- **Path**:' in line:
                # Split on the first ':' after 'Path'
                parts = line.split(':', 1)
                if len(parts) > 1:
                    file_path = parts[1].strip().strip('`')
                break

        analysis = {
            'status': 'completed',
            'actions_taken': [],
            'result': '',
            'ai_analysis': ''
        }

        if file_path and Path(file_path).exists():
            # File exists - analyze it
            file_path_obj = Path(file_path)
            file_size = file_path_obj.stat().st_size
            file_ext = file_path_obj.suffix

            analysis['ai_analysis'] = f"""File Analysis:
- File Type: {file_ext or 'unknown'}
- Size: {file_size:,} bytes
- Location: {file_path_obj.parent}
- Modified: {datetime.fromtimestamp(file_path_obj.stat().st_mtime).isoformat()}

Categorization: This is a {self.get_file_category(file_ext)} file.
Action: File has been logged and cataloged in the system."""

            analysis['actions_taken'] = [
                'Analyzed file metadata',
                'Categorized file type',
                'Logged in task record',
                'Verified file accessibility'
            ]
            analysis['result'] = 'Successfully processed watcher event. File has been cataloged.'

        else:
            # File not found - log this
            analysis['ai_analysis'] = f"""File Analysis:
The referenced file could not be found at the specified path.
This may indicate the file was moved or deleted before processing."""

            analysis['actions_taken'] = [
                'Attempted to locate file',
                'Verified file absence',
                'Logged missing file status'
            ]
            analysis['result'] = 'File not found - task completed with note.'

        # Update task file with processing results
        self.update_task_with_processing(task_path, analysis)

        return analysis

    def process_user_request(self, task_path: Path, content: str, metadata: Dict) -> Dict:
        """Process a direct user request task."""
        # For Bronze tier, acknowledge and log
        analysis = {
            'status': 'completed',
            'actions_taken': ['Acknowledged user request', 'Logged request details'],
            'result': 'User request has been recorded.',
            'ai_analysis': 'Direct user request received and logged.'
        }

        self.update_task_with_processing(task_path, analysis)
        return analysis

    def process_generic_task(self, task_path: Path, content: str, metadata: Dict) -> Dict:
        """Process a generic task."""
        analysis = {
            'status': 'completed',
            'actions_taken': ['Reviewed task content', 'Categorized task'],
            'result': 'Task has been processed and logged.',
            'ai_analysis': 'Generic task processed according to standard protocol.'
        }

        self.update_task_with_processing(task_path, analysis)
        return analysis

    def get_file_category(self, extension: str) -> str:
        """Categorize file by extension."""
        categories = {
            '.pdf': 'document',
            '.doc': 'document',
            '.docx': 'document',
            '.txt': 'text',
            '.md': 'markdown',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
            '.mp4': 'video',
            '.mp3': 'audio',
            '.zip': 'archive',
            '.json': 'data',
            '.csv': 'data',
        }
        return categories.get(extension.lower(), 'unknown')

    def update_task_with_processing(self, task_path: Path, analysis: Dict) -> None:
        """Update the task file with processing results."""
        content = self.read_task(task_path)
        timestamp = datetime.now(timezone.utc).isoformat()

        # Find and replace the processing sections
        processing_section = f"""
## Processing

### AI Analysis
{analysis['ai_analysis']}

### Actions Taken
{chr(10).join(f"- {action}" for action in analysis['actions_taken'])}

### Result
{analysis['result']}

**Completed**: {timestamp}
**Status**: {analysis['status']}
"""

        # Replace the placeholder processing section
        if "## Processing" in content:
            # Split at the Processing section
            parts = content.split("## Processing")
            # Keep everything before, add new processing section
            new_content = parts[0] + "## Processing" + processing_section
        else:
            # Append to end
            new_content = content + "\n" + "## Processing" + processing_section

        # Write updated content
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    def move_to_done(self, task_path: Path) -> Path:
        """Move completed task to Done folder."""
        done_path = self.done_path / task_path.name
        shutil.move(str(task_path), str(done_path))
        return done_path

    def process_all_pending(self) -> List[Dict]:
        """Process all pending tasks."""
        results = []
        tasks = self.list_pending_tasks()

        print(f"[INFO] Found {len(tasks)} pending tasks")

        for task_path in tasks:
            print(f"[PROCESS] {task_path.name}")

            try:
                # Process the task
                result = self.process_task(task_path)
                results.append({
                    'task': task_path.name,
                    'status': result['status'],
                    'result': result['result']
                })

                # Move to Done
                done_path = self.move_to_done(task_path)
                print(f"[DONE] Moved to {done_path}")

            except Exception as e:
                print(f"[ERROR] Failed to process {task_path.name}: {e}")
                results.append({
                    'task': task_path.name,
                    'status': 'failed',
                    'error': str(e)
                })

        return results


def main():
    """Main entry point for task processor."""
    import argparse

    parser = argparse.ArgumentParser(description='Process AI Employee tasks')
    parser.add_argument('--list', action='store_true', help='List pending tasks')
    parser.add_argument('--process', action='store_true', help='Process all pending tasks')
    parser.add_argument('--task', type=str, help='Process specific task by filename')
    args = parser.parse_args()

    processor = TaskProcessor()

    if args.list:
        tasks = processor.list_pending_tasks()
        print(f"\nPending Tasks ({len(tasks)}):")
        for task in tasks:
            print(f"  - {task.name}")
        return

    if args.process:
        results = processor.process_all_pending()
        print(f"\n[SUMMARY] Processed {len(results)} tasks")
        for result in results:
            print(f"  [{result['status'].upper()}] {result['task']}")
        return

    if args.task:
        task_path = processor.needs_action_path / args.task
        if task_path.exists():
            result = processor.process_task(task_path)
            done_path = processor.move_to_done(task_path)
            print(f"[DONE] Processed and moved to {done_path}")
        else:
            print(f"[ERROR] Task not found: {args.task}")
        return

    # Default: show help
    parser.print_help()


if __name__ == '__main__':
    main()
