#!/usr/bin/env python3
"""
Audit Logger - Gold Tier Observability

Comprehensive JSON audit logging for all autonomous actions
with graceful degradation and system health monitoring.

Requirements:
- python-dotenv: pip install python-dotenv
- json: Built-in
"""

import os
import json
import traceback
from datetime import datetime, timezone
from pathlib import Path
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
AUDIT_DIR = Path('audit_logs')
AUDIT_DIR.mkdir(exist_ok=True)
CURRENT_AUDIT_LOG = AUDIT_DIR / f"audit_{datetime.now(timezone.utc).strftime('%Y%m%d')}.jsonl"
SYSTEM_HEALTH_FILE = AUDIT_DIR / 'system_health.json'


class AuditLogger:
    """Centralized audit logging with graceful degradation."""

    def __init__(self):
        self.current_log = CURRENT_AUDIT_LOG
        self.health_file = SYSTEM_HEALTH_FILE
        self.error_count = 0
        self.warning_count = 0

    def log(self, level, action, details=None, status=None):
        """
        Log an event with full context.

        Args:
            level: 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
            action: Action being performed
            details: Additional context (dict)
            status: 'success', 'failed', 'partial'
        """
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': level,
            'action': action,
            'status': status or 'unknown',
            'details': details or {},
            'hostname': os.environ.get('HOSTNAME', 'localhost'),
            'process_id': os.getpid()
        }

        try:
            with open(self.current_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')

            # Update error counts
            if level == 'ERROR':
                self.error_count += 1
            elif level == 'WARNING':
                self.warning_count += 1

        except Exception as e:
            # Graceful degradation - if logging fails, continue
            print(f"[LOGGING FAILED] {e}")
            return False

        return True

    def log_info(self, action, details=None):
        """Log info level event."""
        return self.log('INFO', action, details, 'success')

    def log_warning(self, action, details=None):
        """Log warning level event."""
        return self.log('WARNING', action, details, 'warning')

    def log_error(self, action, error, details=None):
        """Log error level event."""
        error_details = details or {}
        error_details['error'] = str(error)
        error_details['traceback'] = traceback.format_exc()
        return self.log('ERROR', action, error_details, 'failed')

    def log_critical(self, action, error, details=None):
        """Log critical level event."""
        error_details = details or {}
        error_details['error'] = str(error)
        error_details['traceback'] = traceback.format_exc()
        return self.log('CRITICAL', action, error_details, 'critical')

    @contextmanager
    def audit_context(self, action, details=None):
        """
        Context manager for automatic success/failure logging.

        Usage:
            with audit_logger.audit_context('process_task', {'task': 'task-1'}):
                # Do work
                pass
        """
        start_time = datetime.now(timezone.utc)

        try:
            yield self
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            self.log_info(action, {**(details or {}), 'duration_seconds': duration})
        except Exception as e:
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            self.log_error(action, e, {**(details or {}), 'duration_seconds': duration})
            raise

    def update_system_health(self, health_metrics):
        """Update system health metrics."""
        health_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'metrics': health_metrics,
            'error_count_24h': self.error_count,
            'warning_count_24h': self.warning_count,
            'status': 'healthy' if self.error_count < 10 else 'degraded' if self.error_count < 50 else 'critical'
        }

        try:
            with open(self.health_file, 'w', encoding='utf-8') as f:
                json.dump(health_data, f, indent=2)
        except:
            pass  # Graceful degradation

        return health_data

    def get_system_health(self):
        """Get current system health status."""
        try:
            with open(self.health_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                'status': 'unknown',
                'error_count_24h': self.error_count,
                'warning_count_24h': self.warning_count
            }

    def query_audit_log(self, action=None, level=None, limit=100):
        """
        Query audit log with filters.

        Args:
            action: Filter by action name
            level: Filter by log level
            limit: Max results to return
        """
        results = []

        try:
            with open(self.current_log, 'r', encoding='utf-8') as f:
                for line in f:
                    if len(results) >= limit:
                        break

                    entry = json.loads(line)

                    # Apply filters
                    if action and entry.get('action') != action:
                        continue
                    if level and entry.get('level') != level:
                        continue

                    results.append(entry)

        except FileNotFoundError:
            return []
        except Exception as e:
            self.log_error('query_audit_log', e)
            return []

        return results

    def get_summary(self):
        """Get audit log summary statistics."""
        try:
            with open(self.current_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            total_events = len(lines)
            level_counts = {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0}

            for line in lines:
                entry = json.loads(line)
                level = entry.get('level', 'INFO')
                level_counts[level] = level_counts.get(level, 0) + 1

            return {
                'total_events': total_events,
                'level_counts': level_counts,
                'log_file': str(self.current_log),
                'date': datetime.now(timezone.utc).strftime('%Y-%m-%d')
            }

        except Exception as e:
            return {
                'error': str(e),
                'log_file': str(self.current_log)
            }


def main():
    """Main entry point for audit logger CLI."""
    import argparse

    parser = argparse.ArgumentParser(description='Audit log management')
    parser.add_argument('--summary', action='store_true',
                       help='Show audit log summary')
    parser.add_argument('--query', metavar='ACTION',
                       help='Query logs by action name')
    parser.add_argument('--level', metavar='LEVEL',
                       choices=['INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                       help='Filter by log level')
    parser.add_argument('--health', action='store_true',
                       help='Show system health status')
    parser.add_argument('--test', action='store_true',
                       help='Run test logging')
    args = parser.parse_args()

    auditor = AuditLogger()

    if args.summary:
        summary = auditor.get_summary()
        print("\n=== AUDIT LOG SUMMARY ===")
        print(json.dumps(summary, indent=2))
        return

    if args.query or args.level:
        results = auditor.query_audit_log(action=args.query, level=args.level, limit=50)
        print(f"\n=== AUDIT LOG QUERY RESULTS ({len(results)} entries) ===")
        for entry in results:
            print(f"{entry['timestamp']} | {entry['level']:8} | {entry['action']:20} | {entry.get('details', {})}")
        return

    if args.health:
        health = auditor.get_system_health()
        print("\n=== SYSTEM HEALTH ===")
        print(json.dumps(health, indent=2))
        return

    if args.test:
        print("[TEST] Running test logging...")

        auditor.log_info('test_action', {'test': 'data'})
        auditor.log_warning('test_warning', {'test': 'warning data'})
        try:
            raise Exception("Test error")
        except Exception as e:
            auditor.log_error('test_error', e, {'context': 'testing'})

        print("[OK] Test complete. Check with --summary")
        return

    parser.print_help()


if __name__ == '__main__':
    main()
