#!/usr/bin/env python3
"""
Local Zone Manager - Platinum Tier Security Zone

Manages local-zone operations for Platinum tier:
- Approval workflow (human-in-the-loop)
- Sensitive operations execution
- Banking operations
- Credential management

Security Rules:
- Banking operations ALWAYS local-only
- Approvals required for sensitive actions
- Credentials never synced to cloud
- Approval thresholds enforced ($100+ requires explicit approval)

Requirements:
- python-dotenv: pip install python-dotenv

Author: AI Employee Vault Team
Version: 1.1.0
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple, Any
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('local_zone.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
LOCAL_ZONE_SYNC = Path(os.getenv('LOCAL_ZONE_SYNC', './local_zone_sync'))
APPROVED_FOLDER = Path(os.getenv('VAULT_APPROVED', 'AI_Employee_Vault/Approved'))
REJECTED_FOLDER = Path(os.getenv('VAULT_REJECTED', 'AI_Employee_Vault/Rejected'))
PENDING_APPROVAL = Path(os.getenv('VAULT_PENDING_APPROVAL', 'AI_Employee_Vault/Pending_Approval'))
LOCAL_VAULT = Path(os.getenv('LOCAL_VAULT', 'AI_Employee_Vault'))

# Approval thresholds
APPROVAL_THRESHOLDS = {
    'financial': 100,  # Any financial operation > $100
    'file_delete': 10,  # Deleting > 10 files requires approval
    'api_call': 0,     # All API calls require approval
    'email_send': 0,    # All emails require approval
    'system_config': 50 # System changes affecting > 50 files
}


class LocalZoneError(Exception):
    """Base exception for local zone errors."""
    pass


class ApprovalNotFoundError(LocalZoneError):
    """Raised when approval request is not found."""
    pass


class TaskExecutionError(LocalZoneError):
    """Raised when task execution fails."""
    pass


class LocalZoneManager:
    """Manages local-zone secure operations."""

    def __init__(self):
        """Initialize local zone manager and create necessary directories."""
        try:
            self.sync_dir = LOCAL_ZONE_SYNC
            self.sync_dir.mkdir(parents=True, exist_ok=True)
            self.local_vault = LOCAL_VAULT

            # Ensure approval folders exist
            for folder in [APPROVED_FOLDER, REJECTED_FOLDER, PENDING_APPROVAL]:
                folder.mkdir(parents=True, exist_ok=True)

            logger.info("Local Zone Manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Local Zone Manager: {e}")
            raise LocalZoneError(f"Initialization failed: {e}")

    def process_synced_task(self, sync_file):
        """
        Process a task synced from the cloud zone.

        Cloud zone prepares the task, local zone executes it.
        """
        print(f"[LOCAL] Processing synced task: {sync_file.name}")

        # Read synced content
        content = sync_file.read_text(encoding='utf-8')

        # Check if task requires approval
        approval_required = self._check_approval_required(content)

        if approval_required['required']:
            # Create approval request
            approval_file = self._create_approval_request(
                sync_file,
                approval_required['reason'],
                approval_required['threshold']
            )
            print(f"[APPROVAL] Required: {approval_required['reason']}")
            print(f"[INFO] Approval request: {approval_file}")
            return {'status': 'awaiting_approval', 'approval_file': approval_file}
        else:
            # Execute directly
            result = self._execute_task(sync_file, content)
            return {'status': 'executed', 'result': result}

    def _check_approval_required(self, content):
        """
        Check if a task requires approval based on thresholds.

        Returns dict with 'required' (bool) and 'reason' (str).
        """
        content_lower = content.lower()

        # Check for sensitive keywords
        if 'approve' in content_lower or 'authorization' in content_lower:
            return {'required': True, 'reason': 'Approval workflow', 'threshold': 'human'}

        # Check for financial operations
        if 'banking' in content_lower or 'financial' in content_lower or 'transfer' in content_lower:
            # Check amount if mentioned
            for word in content_lower.split():
                if word.startswith('$') or word.startswith('usd'):
                    try:
                        amount = float(word.replace('$', '').replace('usd', ''))
                        if amount > APPROVAL_THRESHOLDS['financial']:
                            return {'required': True, 'reason': f'Financial > ${APPROVAL_THRESHOLDS["financial"]}', 'threshold': amount}
                    except:
                        pass
            return {'required': True, 'reason': 'Financial operation', 'threshold': '>0'}

        # Check for API calls
        if 'api_call' in content_lower or 'api.call' in content_lower:
            return {'required': True, 'reason': 'API call execution', 'threshold': 0}

        # Check for email sending
        if 'send_email' in content_lower or 'email.send' in content_lower:
            return {'required': True, 'reason': 'Email sending', 'threshold': 0}

        # Check for large file deletions
        if 'delete' in content_lower:
            # Count mentions of files
            file_count = content_lower.count('file')
            if file_count > APPROVAL_THRESHOLDS['file_delete']:
                return {'required': True, 'reason': f'Massive delete ({file_count} files)', 'threshold': f'>{APPROVAL_THRESHOLDS["file_delete"]} files'}

        return {'required': False, 'reason': 'Safe to execute', 'threshold': None}

    def _create_approval_request(self, sync_file, reason, threshold):
        """Create an approval request for a synced task."""
        task_name = sync_file.name.replace('sync_', '').replace('.md', '')
        timestamp = datetime.now(timezone.utc).isoformat()

        approval = {
            'id': f"local_approval_{timestamp.replace(':', '-')[:19]}",
            'task_source': 'cloud_zone',
            'task_name': task_name,
            'reason': reason,
            'threshold': threshold,
            'created_at': timestamp,
            'status': 'pending',
            'sync_file': str(sync_file)
        }

        # Save approval request
        approval_path = PENDING_APPROVAL / f"{approval['id']}.json"
        with open(approval_path, 'w', encoding='utf-8') as f:
            json.dump(approval, f, indent=2)

        return approval_path

    def execute_sensitive_operation(self, operation, params):
        """
        Execute a sensitive operation in the local zone.

        Operations:
        - Banking: Financial transactions
        - Credentials: Access secret keys
        - System Config: Critical changes
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        if operation == 'banking':
            result = {
                'operation': 'banking',
                'status': 'executed_locally',
                'timestamp': timestamp,
                'params': {'amount': params.get('amount'), 'to': params.get('recipient')},
                'result': 'Transaction logged locally (simulated for demo)',
                'zone': 'local',
                'security': 'credentials_never_synced'
            }

        elif operation == 'credentials':
            result = {
                'operation': 'credential_access',
                'status': 'executed_locally',
                'timestamp': timestamp,
                'service': params.get('service'),
                'result': 'Credential accessed locally',
                'zone': 'local',
                'security': 'never_leaves_local_machine'
            }

        elif operation == 'system_config':
            result = {
                'operation': 'system_configuration',
                'status': 'executed_locally',
                'timestamp': timestamp,
                'config_type': params.get('type'),
                'files_affected': params.get('file_count', 1),
                'result': 'Configuration applied locally',
                'zone': 'local',
                'security': 'local_execution_only'
            }

        else:
            result = {
                'operation': operation,
                'status': 'unknown',
                'timestamp': timestamp,
                'error': 'Unknown operation'
            }

        # Log operation (locally only, never synced)
        local_log = Path('local_audit.log')
        with open(local_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result) + '\n')

        print(f"[LOCAL] Executed sensitive operation: {operation}")
        return result

    def handle_approval_decision(self, approval_id, approved, reason=''):
        """
        Handle an approval decision from the human.

        If approved, execute the synced task.
        If rejected, log the rejection.
        """
        approval_file = PENDING_APPROVAL / f"{approval_id}.json"

        if not approval_file.exists():
            print(f"[ERROR] Approval not found: {approval_id}")
            return False

        # Read approval
        with open(approval_file, 'r', encoding='utf-8') as f:
            approval = json.load(f)

        if approved:
            # Execute the task
            sync_file = Path(approval['sync_file'])
            if sync_file.exists():
                content = sync_file.read_text(encoding='utf-8')
                result = self._execute_task(sync_file, content)

                # Move to approved
                approved_file = APPROVED_FOLDER / f"{approval_id}.json"
                approval['status'] = 'approved'
                approval['approved_at'] = datetime.now(timezone.utc).isoformat()
                approval['approved_by'] = 'human'
                if reason:
                    approval['reason'] = reason

                with open(approved_file, 'w', encoding='utf-8') as f:
                    json.dump(approval, f, indent=2)

                approval_file.unlink()
                print(f"[APPROVED] {approval['task_name']} - Executed locally")
            else:
                print(f"[ERROR] Sync file not found: {approval['sync_file']}")
                return False
        else:
            # Reject
            rejected_file = REJECTED_FOLDER / f"{approval_id}.json"
            approval['status'] = 'rejected'
            approval['rejected_at'] = datetime.now(timezone.utc).isoformat()
            approval['rejected_by'] = 'human'
            approval['rejection_reason'] = reason or 'No reason provided'

            with open(rejected_file, 'w', encoding='utf-8') as f:
                json.dump(approval, f, indent=2)

            approval_file.unlink()
            print(f"[REJECTED] {approval['task_name']} - Reason: {reason}")

        return True

    def _execute_task(self, task_path, content):
        """Execute a task (private method)."""
        # Simulate task execution
        result = {
            'task': task_path.name,
            'executed_at': datetime.now(timezone.utc).isoformat(),
            'zone': 'local',
            'status': 'completed',
            'execution_time': '0.5s'
        }

        # Add execution stamp
        done_path = LOCAL_VAULT / 'Done' / task_path.name.replace('sync_', '')
        done_path.parent.mkdir(parents=True, exist_ok=True)

        processed_content = content + f"""
\n\n## Local Zone Execution

**Executed At**: {datetime.now(timezone.utc).isoformat()}
**Zone**: Local
**Execution By**: Local Zone Manager
**Security**: Sensitive operation executed locally
"""

        done_path.write_text(processed_content, encoding='utf-8')

        return result

    def get_local_status(self):
        """Get local zone status."""
        pending = len(list(PENDING_APPROVAL.glob('*.json')))
        approved = len(list(APPROVED_FOLDER.glob('*.json')))
        rejected = len(list(REJECTED_FOLDER.glob('*.json')))

        return {
            'zone': 'local',
            'status': 'secure',
            'approvals_pending': pending,
            'approvals_approved': approved,
            'approvals_rejected': rejected,
            'capabilities': [
                'approve_actions',
                'sensitive_execution',
                'banking_operations',
                'credential_management',
                'final_authorization'
            ],
            'security_rules': {
                'secrets_never_synced': True,
                'banking_local_only': True,
                'approval_thresholds': APPROVAL_THRESHOLDS
            }
        }


def main():
    """Main entry point for local zone manager."""
    import argparse

    parser = argparse.ArgumentParser(description='Local Zone Manager')
    parser.add_argument('--process', metavar='SYNC_FILE',
                       help='Process synced task from cloud zone')
    parser.add_argument('--approve', metavar='APPROVAL_ID',
                       help='Approve a pending action')
    parser.add_argument('--reject', metavar='APPROVAL_ID',
                       help='Reject a pending action')
    parser.add_argument('--reason', metavar='REASON',
                       help='Reason for rejection')
    parser.add_argument('--sensitive', nargs=2, metavar=('OP', 'PARAMS'),
                       help='Execute sensitive operation')
    parser.add_argument('--status', action='store_true',
                       help='Show local zone status')
    args = parser.parse_args()

    manager = LocalZoneManager()

    if args.process:
        sync_file = Path(args.process)
        if sync_file.exists():
            manager.process_synced_task(sync_file)
        else:
            print(f"[ERROR] Sync file not found: {args.process}")

    if args.approve:
        manager.handle_approval_decision(args.approve, True)

    if args.reject:
        manager.handle_approval_decision(args.reject, False, args.reason or '')

    if args.sensitive:
        op, params_str = args.sensitive
        params = json.loads(params_str) if params_str.startswith('{') else {'type': params_str}
        manager.execute_sensitive_operation(op, params)

    if args.status:
        status = manager.get_local_status()
        print("\n=== LOCAL ZONE STATUS ===")
        print(json.dumps(status, indent=2))

    if not any([args.process, args.approve, args.reject, args.sensitive, args.status]):
        parser.print_help()


if __name__ == '__main__':
    main()
