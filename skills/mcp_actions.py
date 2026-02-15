#!/usr/bin/env python3
"""
MCP Actions Skill - Silver Tier External Action Layer

Agent Skill that integrates with MCP servers for external actions.
Demonstrates Claude performing real external actions via MCP.

Requirements:
- MCP server configured and running
- python-dotenv: pip install python-dotenv
"""

import os
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
NEEDS_ACTION_FOLDER = os.getenv('VAULT_NEEDS_ACTION', 'AI_Employee_Vault/Needs_Action')
DONE_FOLDER = os.getenv('VAULT_DONE', 'AI_Employee_Vault/Done')
MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:3000')


class MCPActions:
    """Executes external actions via MCP servers."""

    def __init__(self):
        self.needs_action_path = Path(NEEDS_ACTION_FOLDER)
        self.done_path = Path(DONE_FOLDER)

    def call_mcp_server(self, action: str, params: dict) -> dict:
        """
        Call an MCP server to perform an external action.

        For Silver tier demo, this simulates MCP calls.
        In production, replace with actual MCP server integration.
        """
        print(f"[MCP] Calling action: {action}")
        print(f"[MCP] Params: {json.dumps(params, indent=2)}")

        # Simulate MCP call (replace with actual MCP integration)
        # This demonstrates the pattern for external actions

        result = {
            'success': True,
            'action': action,
            'params': params,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'result': f"Simulated {action} completed successfully"
        }

        return result

    def write_file(self, filepath: str, content: str) -> dict:
        """External action: Write a file."""
        try:
            file_path = Path(filepath)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return {
                'success': True,
                'action': 'write_file',
                'filepath': filepath,
                'size': len(content),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'action': 'write_file',
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

    def send_notification(self, message: str, title: str = "AI Employee Notification") -> dict:
        """
        External action: Send a notification.

        For demo purposes, this writes to a notification log.
        In production, integrate with actual notification system.
        """
        try:
            notification = {
                'title': title,
                'message': message,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

            # Write to notification log
            notif_file = Path('notifications.jsonl')
            with open(notif_file, 'a') as f:
                f.write(json.dumps(notification) + '\n')

            return {
                'success': True,
                'action': 'send_notification',
                'notification': notification,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'action': 'send_notification',
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

    def execute_command(self, command: str) -> dict:
        """
        External action: Execute a system command.

        WARNING: Use with caution. Only allow safe, whitelisted commands.
        """
        # Whitelist of safe commands
        safe_commands = ['echo', 'date', 'whoami', 'pwd']

        command_base = command.split()[0]
        if command_base not in safe_commands:
            return {
                'success': False,
                'action': 'execute_command',
                'error': f'Command not whitelisted: {command_base}',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )

            return {
                'success': True,
                'action': 'execute_command',
                'command': command,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'action': 'execute_command',
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

    def create_directory(self, dirpath: str) -> dict:
        """External action: Create a directory."""
        try:
            path = Path(dirpath)
            path.mkdir(parents=True, exist_ok=True)

            return {
                'success': True,
                'action': 'create_directory',
                'path': dirpath,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'action': 'create_directory',
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }

    def process_task_with_external_action(self, task_path: Path) -> dict:
        """
        Process a task that may require external actions.

        Analyzes task content and performs appropriate external actions.
        """
        content = task_path.read_text(encoding='utf-8')

        # Check if task requires external action
        if '## External Action Required' not in content:
            return {'requires_action': False}

        # Extract action requirements
        action_section = content.split('## External Action Required')[1].split('##')[0]
        action_type = self.extract_action_type(action_section)

        # Perform the external action
        if action_type == 'write_file':
            filepath = self.extract_field(action_section, 'File')
            file_content = self.extract_field(action_section, 'Content')
            result = self.write_file(filepath, file_content)

        elif action_type == 'send_notification':
            message = self.extract_field(action_section, 'Message')
            title = self.extract_field(action_section, 'Title', default='AI Employee Notification')
            result = self.send_notification(message, title)

        elif action_type == 'execute_command':
            command = self.extract_field(action_section, 'Command')
            result = self.execute_command(command)

        elif action_type == 'create_directory':
            dirpath = self.extract_field(action_section, 'Path')
            result = self.create_directory(dirpath)

        else:
            result = {
                'success': False,
                'error': f'Unknown action type: {action_type}'
            }

        result['requires_action'] = True
        return result

    def extract_action_type(self, section: str) -> str:
        """Extract action type from task section."""
        for line in section.split('\n'):
            if '**Type**:' in line or '- **Type**:' in line:
                return line.split(':')[1].strip()
        return ''

    def extract_field(self, section: str, field: str, default: str = '') -> str:
        """Extract a field value from task section."""
        for line in section.split('\n'):
            if f'**{field}**:' in line or f'- **{field}**:' in line:
                return line.split(':', 1)[1].strip()
        return default


def main():
    """Main entry point for MCP actions."""
    import argparse

    parser = argparse.ArgumentParser(description='Execute external actions via MCP')
    parser.add_argument('--write-file', nargs=2, metavar=('FILE', 'CONTENT'),
                       help='Write content to file')
    parser.add_argument('--notify', metavar='MESSAGE',
                       help='Send a notification')
    parser.add_argument('--cmd', metavar='COMMAND',
                       help='Execute a safe command')
    parser.add_argument('--mkdir', metavar='PATH',
                       help='Create a directory')
    args = parser.parse_args()

    mcp = MCPActions()

    if args.write_file:
        filepath, content = args.write_file
        result = mcp.write_file(filepath, content)
        print(json.dumps(result, indent=2))

    elif args.notify:
        result = mcp.send_notification(args.notify)
        print(json.dumps(result, indent=2))

    elif args.cmd:
        result = mcp.execute_command(args.cmd)
        print(json.dumps(result, indent=2))

    elif args.mkdir:
        result = mcp.create_directory(args.mkdir)
        print(json.dumps(result, indent=2))

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
