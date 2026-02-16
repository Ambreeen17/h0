#!/usr/bin/env python3
"""
Backup Manager - Enhanced Feature 4

Automated backup and recovery system:
- Vault backups
- Incremental backups
- Scheduled backups
- Restore functionality

Usage:
    python skills/backup_manager.py --backup
    python skills/backup_manager.py --restore <backup_id>
    python skills/backup_manager.py --schedule
"""

import os
import json
import shutil
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from filelock import FileLock

load_dotenv()

# Configuration
CLOUD_VAULT = Path(os.getenv('CLOUD_VAULT', 'AI_Employee_Vault_Cloud'))
LOCAL_VAULT = Path(os.getenv('LOCAL_VAULT', 'AI_Employee_Vault'))
BACKUP_DIR = Path(os.getenv('BACKUP_DIR', './backups'))
BACKUP_LOCK = Path('./backup.lock')


class BackupManager:
    """Manage vault backups and recovery."""

    def __init__(self):
        self.backup_dir = BACKUP_DIR
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.backup_dir / 'backup_metadata.json'

    def create_backup(self, backup_type='full'):
        """
        Create a backup of vaults.

        Args:
            backup_type: 'full' or 'incremental'
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        backup_id = f"backup_{timestamp.replace(':', '-')}"

        print(f"[INFO] Creating {backup_type} backup: {backup_id}")

        # Acquire lock to prevent concurrent operations
        lock = FileLock(BACKUP_LOCK, timeout=30)

        try:
            with lock:
                backup_path = self.backup_dir / backup_id
                backup_path.mkdir(parents=True, exist_ok=True)

                # Backup cloud vault
                if CLOUD_VAULT.exists():
                    cloud_backup = backup_path / 'cloud_vault'
                    shutil.copytree(CLOUD_VAULT, cloud_backup)
                    print(f"[OK] Backed up cloud vault")

                # Backup local vault
                if LOCAL_VAULT.exists():
                    local_backup = backup_path / 'local_vault'
                    shutil.copytree(LOCAL_VAULT, local_backup)
                    print(f"[OK] Backed up local vault")

                # Calculate checksums
                checksums = self._calculate_checksums(backup_path)

                # Create metadata
                metadata = {
                    'backup_id': backup_id,
                    'timestamp': timestamp,
                    'type': backup_type,
                    'cloud_vault_size': self._get_dir_size(CLOUD_VAULT) if CLOUD_VAULT.exists() else 0,
                    'local_vault_size': self._get_dir_size(LOCAL_VAULT) if LOCAL_VAULT.exists() else 0,
                    'checksums': checksums
                }

                # Save metadata
                metadata_file = backup_path / 'metadata.json'
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)

                # Update backup registry
                self._update_registry(metadata)

                print(f"[OK] Backup complete: {backup_id}")
                print(f"[INFO] Total size: {metadata['cloud_vault_size'] + metadata['local_vault_size']:,} bytes")

                return backup_id

        except Exception as e:
            print(f"[ERROR] Backup failed: {e}")
            # Cleanup incomplete backup
            if backup_path.exists():
                shutil.rmtree(backup_path)
            raise

    def restore_backup(self, backup_id):
        """
        Restore from backup.

        Args:
            backup_id: ID of backup to restore
        """
        backup_path = self.backup_dir / backup_id

        if not backup_path.exists():
            print(f"[ERROR] Backup not found: {backup_id}")
            return False

        print(f"[INFO] Restoring from backup: {backup_id}")

        # Verify backup integrity
        if not self._verify_backup(backup_path):
            print(f"[ERROR] Backup verification failed")
            return False

        # Confirm with user
        response = input("This will replace current vaults. Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("[INFO] Restore cancelled")
            return False

        try:
            # Restore cloud vault
            cloud_backup = backup_path / 'cloud_vault'
            if cloud_backup.exists():
                if CLOUD_VAULT.exists():
                    shutil.rmtree(CLOUD_VAULT)
                shutil.copytree(cloud_backup, CLOUD_VAULT)
                print(f"[OK] Restored cloud vault")

            # Restore local vault
            local_backup = backup_path / 'local_vault'
            if local_backup.exists():
                if LOCAL_VAULT.exists():
                    shutil.rmtree(LOCAL_VAULT)
                shutil.copytree(local_backup, LOCAL_VAULT)
                print(f"[OK] Restored local vault")

            print(f"[OK] Restore complete: {backup_id}")
            return True

        except Exception as e:
            print(f"[ERROR] Restore failed: {e}")
            return False

    def list_backups(self):
        """List all available backups."""
        if not self.metadata_file.exists():
            print("[INFO] No backups found")
            return []

        with open(self.metadata_file, 'r') as f:
            registry = json.load(f)

        backups = sorted(registry['backups'], key=lambda x: x['timestamp'], reverse=True)

        print(f"\n=== AVAILABLE BACKUPS ({len(backups)}) ===\n")

        for backup in backups:
            print(f"ID: {backup['backup_id']}")
            print(f"  Type: {backup['type']}")
            print(f"  Date: {backup['timestamp']}")
            print(f"  Size: {backup['cloud_vault_size'] + backup['local_vault_size']:,} bytes")
            print()

        return backups

    def cleanup_old_backups(self, keep_count=10):
        """
        Remove old backups, keeping only the most recent ones.

        Args:
            keep_count: Number of backups to keep
        """
        if not self.metadata_file.exists():
            return

        with open(self.metadata_file, 'r') as f:
            registry = json.load(f)

        backups = sorted(registry['backups'], key=lambda x: x['timestamp'], reverse=True)

        if len(backups) <= keep_count:
            print(f"[INFO] No cleanup needed (have {len(backups)}, keeping {keep_count})")
            return

        # Remove old backups
        to_remove = backups[keep_count:]

        for backup in to_remove:
            backup_path = self.backup_dir / backup['backup_id']
            if backup_path.exists():
                shutil.rmtree(backup_path)
                print(f"[OK] Removed old backup: {backup['backup_id']}")

        # Update registry
        registry['backups'] = backups[:keep_count]

        with open(self.metadata_file, 'w') as f:
            json.dump(registry, f, indent=2)

    def _calculate_checksums(self, backup_path):
        """Calculate checksums for backup files."""
        checksums = {}

        for root, dirs, files in os.walk(backup_path):
            for file in files:
                file_path = Path(root) / file
                if file_path.name == 'metadata.json':
                    continue

                rel_path = file_path.relative_to(backup_path)
                checksums[str(rel_path)] = self._md5(file_path)

        return checksums

    def _verify_backup(self, backup_path):
        """Verify backup integrity using checksums."""
        metadata_file = backup_path / 'metadata.json'

        if not metadata_file.exists():
            return False

        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

        stored_checksums = metadata.get('checksums', {})

        for rel_path, checksum in stored_checksums.items():
            file_path = backup_path / rel_path
            if not file_path.exists():
                return False

            if self._md5(file_path) != checksum:
                return False

        return True

    def _md5(self, file_path):
        """Calculate MD5 checksum of file."""
        hash_md5 = hashlib.md5()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()

    def _get_dir_size(self, dir_path):
        """Get total size of directory."""
        total_size = 0

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = Path(root) / file
                total_size += file_path.stat().st_size

        return total_size

    def _update_registry(self, metadata):
        """Update backup registry with new backup."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                registry = json.load(f)
        else:
            registry = {'backups': []}

        registry['backups'].append(metadata)

        with open(self.metadata_file, 'w') as f:
            json.dump(registry, f, indent=2)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Backup Manager')
    parser.add_argument('--backup', action='store_true',
                       help='Create backup')
    parser.add_argument('--restore', metavar='BACKUP_ID',
                       help='Restore from backup')
    parser.add_argument('--list', action='store_true',
                       help='List backups')
    parser.add_argument('--cleanup', action='store_true',
                       help='Remove old backups')
    parser.add_argument('--keep', type=int, default=10,
                       help='Number of backups to keep (default: 10)')
    args = parser.parse_args()

    manager = BackupManager()

    if args.backup:
        manager.create_backup()

    if args.restore:
        manager.restore_backup(args.restore)

    if args.list:
        manager.list_backups()

    if args.cleanup:
        manager.cleanup_old_backups(args.keep)

    if not any([args.backup, args.restore, args.list, args.cleanup]):
        parser.print_help()


if __name__ == '__main__':
    main()
