#!/usr/bin/env python3
"""
Zone Sync Manager - Platinum Tier Delegation Architecture

Manages secure synchronization between cloud and local zones.

Delegation Architecture Rules:
1. Claim-by-Move: Agents claim tasks by moving files between zones
2. Single-Writer Dashboard: Only one writer at a time (uses file locking)
3. Markdown-Only Sync: Only .md files synced between zones
4. Secrets Never Synced: Local zone secrets never transmitted

Requirements:
- python-dotenv: pip install python-dotenv
- filelock: pip install filelock
"""

import os
import json
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from filelock import FileLock, Timeout

# Load environment variables
load_dotenv()

# Configuration
CLOUD_ZONE = Path(os.getenv('CLOUD_VAULT', 'AI_Employee_Vault_Cloud'))
LOCAL_ZONE = Path(os.getenv('LOCAL_VAULT', 'AI_Employee_Vault'))
SYNC_QUEUE = Path('zone_sync_queue')
DASHBOARD_LOCK = Path('dashboard.lock')

# Sync rules
SYNC_RULES = {
    'markdown_only': True,  # Only sync .md files
    'max_file_size': 1024 * 1024,  # 1MB max file size
    'exclude_patterns': ['.env', 'credential', 'secret', 'token'],
    'scan_interval': 5  # seconds
}


class ZoneSyncManager:
    """Manages secure synchronization between zones."""

    def __init__(self):
        self.sync_queue = SYNC_QUEUE
        self.sync_queue.mkdir(parents=True, exist_ok=True)

    def claim_task(self, task_path, from_zone, to_zone):
        """
        Claim a task by moving it between zones.

        Implements Claim-by-Move delegation rule.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        claim = {
            'task': str(task_path),
            'from_zone': from_zone,
            'to_zone': to_zone,
            'claimed_at': timestamp,
            'claimed_by': os.getenv('ZONE', 'unknown')
        }

        # Create claim file
        claim_file = self.sync_queue / f"claim_{task_path.stem}_{timestamp.replace(':', '-')}[.{from_zone}].json"
        with open(claim_file, 'w', encoding='utf-8') as f:
            json.dump(claim, f, indent=2)

        # Move the task (claim by move)
        target_path = Path(to_zone) / task_path.name
        task_path.rename(target_path)

        print(f"[CLAIM] Task {task_path.name}: {from_zone} → {to_zone}")
        print(f"[INFO] Claim file: {claim_file.name}")

        return claim_file, target_path

    def sync_file(self, source_path, dest_zone):
        """
        Sync a file between zones (markdown-only policy).

        Only .md files are synced. All other files are blocked.
        """
        # Check markdown-only rule
        if source_path.suffix != '.md':
            print(f"[BLOCK] Non-markdown file: {source_path.name}")
            return False

        # Check file size
        file_size = source_path.stat().st_size
        if file_size > SYNC_RULES['max_file_size']:
            print(f"[BLOCK] File too large: {file_size} bytes (max: {SYNC_RULES['max_file_size']})")
            return False

        # Check exclude patterns
        for pattern in SYNC_RULES['exclude_patterns']:
            if pattern in source_path.name.lower():
                print(f"[BLOCK] Excluded pattern: {pattern}")
                return False

        # Check for secrets
        content = source_path.read_text(encoding='utf-8')
        secret_patterns = ['password', 'api_key', 'secret', 'token', 'credential', 'private_key']
        for pattern in secret_patterns:
            if pattern in content.lower():
                print(f"[BLOCK] Secret detected: {pattern} - file not synced")
                return False

        # Perform sync
        dest_path = Path(dest_zone) / source_path.name
        dest_path.write_text(content, encoding='utf-8')

        # Create sync receipt
        receipt = {
            'file': source_path.name,
            'synced_at': datetime.now(timezone.utc).isoformat(),
            'size': file_size,
            'checksum': hashlib.md5(content.encode()).hexdigest(),
            'from_zone': str(source_path.parent.parent),
            'to_zone': str(dest_zone)
        }

        receipt_file = self.sync_queue / f"sync_receipt_{source_path.stem}.json"
        with open(receipt_file, 'w', encoding='utf-8') as f:
            json.dump(receipt, f, indent=2)

        print(f"[SYNC] {source_path.name}: {source_path.parent.parent.name} → {dest_zone}")
        print(f"[INFO] Size: {file_size} bytes, MD5: {receipt['checksum'][:8]}...")

        return dest_path

    def update_dashboard_single_writer(self, update_func):
        """
        Update dashboard with single-writer guarantee.

        Uses file locking to ensure only one writer at a time.
        """
        lock = FileLock(DASHBOARD_LOCK, timeout=10)

        try:
            with lock:
                print(f"[LOCK] Dashboard lock acquired")
                result = update_func()

                # Write to dashboard
                dashboard_path = CLOUD_ZONE / 'Dashboard.md'
                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(result)

                print(f"[UNLOCK] Dashboard updated and lock released")
                return True

        except Timeout:
            print("[ERROR] Dashboard lock timeout - could not acquire lock")
            return False
        except Exception as e:
            print(f"[ERROR] Dashboard update failed: {e}")
            return False

    def scan_and_sync(self):
        """
        Scan for files to sync and process them.

        Implements continuous synchronization between zones.
        """
        print(f"[SCAN] Scanning for files to sync...")

        synced_count = 0

        # Scan cloud zone for files to sync to local
        for task_file in CLOUD_ZONE.glob('*.md'):
            if not (LOCAL_ZONE / task_file.name).exists():
                self.sync_file(task_file, LOCAL_ZONE)
                synced_count += 1

        print(f"[SCAN] Synced {synced_count} files between zones")
        return synced_count

    def get_delegation_status(self):
        """Get current delegation and sync status."""
        claims = list(self.sync_queue.glob('claim_*.json'))
        receipts = list(self.sync_queue.glob('sync_receipt_*.json'))

        return {
            'zone_sync_active': True,
            'pending_claims': len(claims),
            'completed_syncs': len(receipts),
            'sync_rules': SYNC_RULES,
            'delegation_architecture': {
                'claim_by_move': 'Agents claim tasks by moving files',
                'single_writer_dashboard': 'File locking ensures one writer',
                'markdown_only_sync': 'Only .md files synced between zones',
                'secrets_never_synced': 'Local zone secrets never transmitted'
            }
        }


def main():
    """Main entry point for zone sync manager."""
    import argparse

    parser = argparse.ArgumentParser(description='Zone Sync Manager')
    parser.add_argument('--claim', nargs=2, metavar=('TASK', 'TO_ZONE'),
                       help='Claim task and move to zone')
    parser.add_argument('--sync', nargs=2, metavar=('FILE', 'TO_ZONE'),
                       help='Sync file to zone')
    parser.add_argument('--scan', action='store_true',
                       help='Scan and sync files between zones')
    parser.add_argument('--status', action='store_true',
                       help='Show delegation status')
    args = parser.parse_args()

    manager = ZoneSyncManager()

    if args.claim:
        task, to_zone = args.claim
        task_path = Path(task)
        if task_path.exists():
            manager.claim_task(task_path, task_path.parent.name, to_zone)
        else:
            print(f"[ERROR] Task not found: {task}")

    if args.sync:
        file_path, to_zone = args.sync
        manager.sync_file(Path(file_path), to_zone)

    if args.scan:
        manager.scan_and_sync()

    if args.status:
        status = manager.get_delegation_status()
        print("\n=== DELEGATION STATUS ===")
        print(json.dumps(status, indent=2))

    if not any([args.claim, args.sync, args.scan, args.status]):
        parser.print_help()


if __name__ == '__main__':
    main()
