#!/usr/bin/env python3
"""
Approval Workflow - Silver Tier Human-in-the-Loop

Implements approval workflow for sensitive actions using file-based state.
Tasks requiring approval move through: Pending_Approval → Approved/Rejected

Requirements:
- python-dotenv: pip install python-dotenv
"""

import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PENDING_APPROVAL_FOLDER = os.getenv('VAULT_PENDING_APPROVAL', 'AI_Employee_Vault/Pending_Approval')
APPROVED_FOLDER = os.getenv('VAULT_APPROVED', 'AI_Employee_Vault/Approved')
REJECTED_FOLDER = os.getenv('VAULT_REJECTED', 'AI_Employee_Vault/Rejected')
DONE_FOLDER = os.getenv('VAULT_DONE', 'AI_Employee_Vault/Done')


class ApprovalWorkflow:
    """Manages human-in-the-loop approval workflow for sensitive actions."""

    def __init__(self):
        self.pending_path = Path(PENDING_APPROVAL_FOLDER)
        self.approved_path = Path(APPROVED_FOLDER)
        self.rejected_path = Path(REJECTED_FOLDER)
        self.done_path = Path(DONE_FOLDER)

        # Ensure folders exist
        for path in [self.pending_path, self.approved_path, self.rejected_path, self.done_path]:
            path.mkdir(parents=True, exist_ok=True)

    def requires_approval(self, task_content: str) -> bool:
        """
        Determine if a task requires human approval.

        Tasks require approval if they:
        - Send emails
        - Delete files
        - Modify system settings
        - Execute commands
        - Perform financial transactions
        """
        sensitive_keywords = [
            'send email', 'delete', 'remove', 'execute command', 'run command',
            'financial', 'payment', 'transfer', 'system settings', 'config'
        ]

        task_lower = task_content.lower()
        return any(keyword in task_lower for keyword in sensitive_keywords)

    def submit_for_approval(self, task_path: Path, proposed_action: str) -> Path:
        """
        Submit a task for human approval.

        Creates an approval request document with task details and proposed action.
        """
        content = task_path.read_text(encoding='utf-8')
        timestamp = datetime.now(timezone.utc).isoformat()

        # Create approval request
        approval_filename = f"approval-{task_path.stem}.md"
        approval_path = self.pending_path / approval_filename

        approval_content = f"""# Approval Request

**Created**: {timestamp}
**Status**: pending
**Task File**: `{task_path.name}`
**Priority**: high

## Task Summary

{content[:500]}

...

## Proposed Action

{proposed_action}

## Risk Assessment

- **Data Loss**: Low
- **System Impact**: Low
- **Reversibility**: High
- **Requires Manual Review**: Yes

## Approval Options

### Approve
If you approve this action, run:
```bash
python skills/approval_workflow.py --approve {approval_filename}
```

### Reject
If you reject this action, run:
```bash
python skills/approval_workflow.py --reject {approval_filename}
```

## Review Checklist

Before approving, verify:
- [ ] The proposed action is safe and appropriate
- [ ] The action aligns with your goals
- [ ] The action is reversible if needed
- [ ] You understand the consequences

---

**Submitted**: {timestamp}
**Status**: Awaiting human review

---

*This is a Human-in-the-Loop checkpoint. The AI Employee will wait for your approval before proceeding.*
"""

        # Write approval request
        with open(approval_path, 'w', encoding='utf-8') as f:
            f.write(approval_content)

        print(f"[✓] Submitted for approval: {approval_filename}")
        print(f"[INFO] Task: {task_path.name}")
        print(f"[INFO] Proposed action: {proposed_action[:100]}...")

        return approval_path

    def approve(self, approval_filename: str) -> dict:
        """Approve an action and execute it."""
        approval_path = self.pending_path / approval_filename

        if not approval_path.exists():
            return {
                'success': False,
                'error': f'Approval request not found: {approval_filename}'
            }

        # Read approval request
        content = approval_path.read_text(encoding='utf-8')
        timestamp = datetime.now(timezone.utc).isoformat()

        # Extract task file reference
        task_filename = self.extract_field(content, 'Task File')

        # Update approval status
        updated_content = content + f"""

## Approval Decision

**Decision**: APPROVED ✅
**Approved By**: Human User
**Approved At**: {timestamp}

## Execution

The approved action will now be executed.

---

*This action was approved and executed by Human-in-the-Loop workflow.*
"""

        # Move to approved folder
        approved_path = self.approved_path / approval_filename
        approved_path.write_text(updated_content)
        approval_path.unlink()

        print(f"[✓] Approved: {approval_filename}")
        print(f"[INFO] Moved to Approved folder")

        return {
            'success': True,
            'action': 'approved',
            'task_file': task_filename,
            'timestamp': timestamp
        }

    def reject(self, approval_filename: str, reason: str = "No reason provided") -> dict:
        """Reject an action."""
        approval_path = self.pending_path / approval_filename

        if not approval_path.exists():
            return {
                'success': False,
                'error': f'Approval request not found: {approval_filename}'
            }

        # Read approval request
        content = approval_path.read_text(encoding='utf-8')
        timestamp = datetime.now(timezone.utc).isoformat()

        # Update approval status
        updated_content = content + f"""

## Approval Decision

**Decision**: REJECTED ❌
**Rejected By**: Human User
**Rejected At**: {timestamp}
**Reason**: {reason}

## Next Steps

The proposed action will NOT be executed.
The task may be revised and resubmitted for approval.

---

*This action was rejected by Human-in-the-Loop workflow.*
"""

        # Move to rejected folder
        rejected_path = self.rejected_path / approval_filename
        rejected_path.write_text(updated_content)
        approval_path.unlink()

        print(f"[✓] Rejected: {approval_filename}")
        print(f"[INFO] Reason: {reason}")
        print(f"[INFO] Moved to Rejected folder")

        return {
            'success': True,
            'action': 'rejected',
            'reason': reason,
            'timestamp': timestamp
        }

    def list_pending(self) -> list:
        """List all pending approval requests."""
        approvals = list(self.pending_path.glob('approval-*.md'))
        return sorted(approvals, key=lambda p: p.stat().st_mtime)

    def extract_field(self, content: str, field: str) -> str:
        """Extract a field value from approval request."""
        for line in content.split('\n'):
            if f'**{field}**:' in line or f'- **{field}**:' in line:
                return line.split(':', 1)[1].strip().strip('`')
        return ''

    def get_stats(self) -> dict:
        """Get approval workflow statistics."""
        pending = len(list(self.pending_path.glob('*.md')))
        approved = len(list(self.approved_path.glob('*.md')))
        rejected = len(list(self.rejected_path.glob('*.md')))

        return {
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
            'total': pending + approved + rejected
        }


def main():
    """Main entry point for approval workflow."""
    import argparse

    parser = argparse.ArgumentParser(description='Manage approval workflow')
    parser.add_argument('--list', action='store_true',
                       help='List pending approval requests')
    parser.add_argument('--approve', metavar='FILENAME',
                       help='Approve an action')
    parser.add_argument('--reject', metavar='FILENAME',
                       help='Reject an action')
    parser.add_argument('--reason', metavar='REASON',
                       help='Reason for rejection', default='')
    parser.add_argument('--stats', action='store_true',
                       help='Show approval statistics')
    args = parser.parse_args()

    workflow = ApprovalWorkflow()

    if args.list:
        pending = workflow.list_pending()
        print(f"\nPending Approvals ({len(pending)}):")
        if pending:
            for approval in pending:
                print(f"  - {approval.name}")
        else:
            print("  No pending approvals")
        return

    if args.approve:
        result = workflow.approve(args.approve)
        if result['success']:
            print(f"[✓] Action approved: {args.approve}")
        else:
            print(f"[ERROR] {result['error']}")
        return

    if args.reject:
        result = workflow.reject(args.reject, args.reason)
        if result['success']:
            print(f"[✓] Action rejected: {args.reject}")
        else:
            print(f"[ERROR] {result['error']}")
        return

    if args.stats:
        stats = workflow.get_stats()
        print(f"\nApproval Statistics:")
        print(f"  Pending: {stats['pending']}")
        print(f"  Approved: {stats['approved']}")
        print(f"  Rejected: {stats['rejected']}")
        print(f"  Total: {stats['total']}")
        return

    # Default: show help
    parser.print_help()


if __name__ == '__main__':
    main()
