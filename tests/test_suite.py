#!/usr/bin/env python3
"""
AI Employee Vault - Comprehensive Test Suite

Tests all Platinum tier components:
- Zone communication
- Approval workflows
- Health monitoring
- Secret filtering
- Delegation architecture
- Dashboard locking
- MCP integrations
- Audit logging

Usage:
    python tests/test_suite.py --all
    python tests/test_suite.py --component cloud_zone
    python tests/test_suite.py --test test_secret_filtering
"""

import os
import sys
import json
import time
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import skills to test
try:
    from skills.cloud_zone_manager import CloudZoneManager
    from skills.local_zone_manager import LocalZoneManager
    from skills.zone_sync_manager import ZoneSyncManager
    from skills.health_monitor import HealthMonitor
    from skills.approval_workflow import ApprovalWorkflow
    from skills.audit_logger import AuditLogger
except ImportError as e:
    print(f"[ERROR] Could not import skills: {e}")
    print("[INFO] Make sure you're running from the project root directory")
    sys.exit(1)

# Load environment variables
load_dotenv()


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class TestResult:
    """Test result container."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors = []

    def add_pass(self):
        self.passed += 1

    def add_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))

    def add_skip(self):
        self.skipped += 1

    def print_summary(self):
        total = self.passed + self.failed + self.skipped
        print(f"\n{'='*70}")
        print(f"Test Summary: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"{Colors.RED}{self.failed} failed{Colors.END}")
        if self.skipped > 0:
            print(f"{Colors.YELLOW}{self.skipped} skipped{Colors.END}")
        print(f"{'='*70}\n")

        if self.errors:
            print(f"{Colors.RED}Failed Tests:{Colors.END}")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")


class TestSuite:
    """Comprehensive test suite for AI Employee Vault."""

    def __init__(self):
        self.results = TestResult()
        self.temp_dir = None
        self.original_dir = os.getcwd()

    def setup(self):
        """Setup test environment."""
        print(f"{Colors.BLUE}Setting up test environment...{Colors.END}")

        # Create temporary directory for tests
        self.temp_dir = tempfile.mkdtemp(prefix='ai_employee_test_')

        # Set environment variables for test paths
        os.environ['CLOUD_VAULT'] = str(Path(self.temp_dir) / 'cloud_vault')
        os.environ['LOCAL_VAULT'] = str(Path(self.temp_dir) / 'local_vault')
        os.environ['CLOUD_ZONE_SYNC'] = str(Path(self.temp_dir) / 'cloud_sync')
        os.environ['LOCAL_ZONE_SYNC'] = str(Path(self.temp_dir) / 'local_sync')

        print(f"[OK] Test directory: {self.temp_dir}")

    def teardown(self):
        """Cleanup test environment."""
        print(f"\n{Colors.BLUE}Cleaning up test environment...{Colors.END}")

        # Change back to original directory
        os.chdir(self.original_dir)

        # Remove temporary directory
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
            print(f"[OK] Cleaned up: {self.temp_dir}")

    def run_test(self, test_name, test_func):
        """Run a single test."""
        try:
            print(f"\n{Colors.BOLD}Running: {test_name}{Colors.END}")
            test_func()
            print(f"{Colors.GREEN}[PASS]{Colors.END} {test_name}")
            self.results.add_pass()
        except AssertionError as e:
            print(f"{Colors.RED}[FAIL]{Colors.END} {test_name}: {e}")
            self.results.add_fail(test_name, str(e))
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.END} {test_name}: {e}")
            self.results.add_fail(test_name, str(e))

    # ========================================================================
    # CLOUD ZONE TESTS
    # ========================================================================

    def test_cloud_zone_initialization(self):
        """Test cloud zone manager initialization."""
        manager = CloudZoneManager()
        assert manager.cloud_vault.exists(), "Cloud vault should be created"
        assert manager.local_vault.exists(), "Local vault should be created"
        assert manager.sync_dir.exists(), "Sync directory should be created"

    def test_cloud_can_handle_safe_tasks(self):
        """Test cloud zone can handle safe tasks."""
        manager = CloudZoneManager()

        # Safe tasks
        safe, reason = manager.can_handle_in_cloud('draft', 'Create LinkedIn post')
        assert safe is True, f"Draft should be safe in cloud: {reason}"

        safe, reason = manager.can_handle_in_cloud('analyze', 'Analyze data')
        assert safe is True, f"Analysis should be safe in cloud: {reason}"

    def test_cloud_blocks_sensitive_tasks(self):
        """Test cloud zone blocks sensitive tasks."""
        manager = CloudZoneManager()

        # Sensitive tasks
        safe, reason = manager.can_handle_in_cloud('approve', 'Send money')
        assert safe is False, "Approval tasks should be blocked"

        safe, reason = manager.can_handle_in_cloud('execute', 'Access credentials')
        assert safe is False, "Credential access should be blocked"

    def test_cloud_draft_creation(self):
        """Test cloud zone draft creation."""
        manager = CloudZoneManager()

        draft_path = manager.draft_content_in_cloud('linkedin', 'Test content')
        assert draft_path.exists(), "Draft file should be created"

        content = draft_path.read_text()
        assert 'Test content' in content, "Draft should contain content"
        assert 'Cloud Zone' in content, "Draft should have zone metadata"

    def test_cloud_triage(self):
        """Test cloud zone triage."""
        manager = CloudZoneManager()

        # Create test task
        task_path = manager.cloud_vault / 'test_task.md'
        task_content = """# Test Task

**Type**: email-event
**Priority**: high

Test email content
"""
        task_path.write_text(task_content)

        # Run triage
        triage = manager.triage_tasks(task_path)

        assert triage['type'] == 'email-event', "Should detect task type"
        assert triage['priority'] == 'high', "Should detect priority"
        assert 'zone_recommendation' in triage, "Should recommend zone"

    # ========================================================================
    # LOCAL ZONE TESTS
    # ========================================================================

    def test_local_zone_initialization(self):
        """Test local zone manager initialization."""
        manager = LocalZoneManager()
        # Local zone manager should initialize without errors
        assert manager is not None

    def test_approval_threshold_enforcement(self):
        """Test approval thresholds are enforced."""
        manager = LocalZoneManager()

        # Create test task requiring approval
        task_path = manager.local_vault / 'financial_task.md'
        task_content = """# Financial Task

**Type**: financial
**Amount**: $150

Requires approval for amounts > $100
"""
        task_path.write_text(task_content)

        # Process task
        result = manager.process_task(task_path)

        assert result['requires_approval'] is True, "Financial > $100 should require approval"

    def test_approval_workflow(self):
        """Test approval workflow."""
        # Create approval request
        approval = ApprovalWorkflow()
        approval_id = approval.create_approval(
            task_name='test_task',
            action_type='email_send',
            params={'to': 'test@example.com'}
        )

        assert approval_id is not None, "Approval ID should be created"

        # Check approval status
        status = approval.get_approval_status(approval_id)
        assert status == 'pending', "Approval should be pending"

        # Approve
        success = approval.approve(approval_id)
        assert success is True, "Approval should succeed"

        # Check final status
        status = approval.get_approval_status(approval_id)
        assert status == 'approved', "Approval should be approved"

    # ========================================================================
    # ZONE SYNC TESTS
    # ========================================================================

    def test_claim_by_move(self):
        """Test claim-by-move delegation."""
        sync_manager = ZoneSyncManager()

        # Create test task in cloud zone
        task_path = sync_manager.CLOUD_ZONE / 'test_claim_task.md'
        task_path.write_text("# Test Task\n\nTest content")

        # Claim task
        claim_file, moved_path = sync_manager.claim_task(
            task_path,
            str(sync_manager.CLOUD_ZONE),
            str(sync_manager.LOCAL_ZONE)
        )

        assert claim_file.exists(), "Claim file should be created"
        assert not task_path.exists(), "Original task should be moved"
        assert moved_path.exists(), "Task should be in destination"

        # Verify claim file content
        claim_data = json.loads(claim_file.read_text())
        assert 'claimed_at' in claim_data, "Claim should have timestamp"
        assert 'from_zone' in claim_data, "Claim should have source zone"

    def test_markdown_only_sync(self):
        """Test markdown-only sync policy."""
        sync_manager = ZoneSyncManager()

        # Create markdown file (should sync)
        md_file = sync_manager.CLOUD_ZONE / 'test.md'
        md_file.write_text("# Markdown file")

        result = sync_manager.sync_file(md_file, sync_manager.LOCAL_ZONE)
        assert result is True, "Markdown file should sync"

        # Create non-markdown file (should be blocked)
        txt_file = sync_manager.CLOUD_ZONE / 'test.txt'
        txt_file.write_text("Text file")

        result = sync_manager.sync_file(txt_file, sync_manager.LOCAL_ZONE)
        assert result is False, "Non-markdown file should be blocked"

    def test_secret_filtering(self):
        """Test secret filtering in sync."""
        sync_manager = ZoneSyncManager()

        # Create file with secrets (should be blocked)
        secret_file = sync_manager.CLOUD_ZONE / 'secret.md'
        secret_file.write_text("API_KEY = sk-1234567890")

        result = sync_manager.sync_file(secret_file, sync_manager.LOCAL_ZONE)
        assert result is False, "File with secrets should be blocked"

        # Create file without secrets (should pass)
        safe_file = sync_manager.CLOUD_ZONE / 'safe.md'
        safe_file.write_text("# Safe content\n\nNo secrets here")

        result = sync_manager.sync_file(safe_file, sync_manager.LOCAL_ZONE)
        assert result is True, "Safe file should sync"

    def test_file_size_limits(self):
        """Test file size limits in sync."""
        sync_manager = ZoneSyncManager()

        # Create large file (should be blocked)
        large_file = sync_manager.CLOUD_ZONE / 'large.md'
        large_file.write_text("x" * (2 * 1024 * 1024))  # 2MB

        result = sync_manager.sync_file(large_file, sync_manager.LOCAL_ZONE)
        assert result is False, "Large file should be blocked"

    def test_single_writer_dashboard(self):
        """Test single-writer dashboard locking."""
        sync_manager = ZoneSyncManager()

        # Test dashboard update with locking
        def update_func():
            return "# Dashboard\n\nUpdated at " + datetime.now().isoformat()

        # Should succeed
        result = sync_manager.update_dashboard_single_writer(update_func)
        assert result is True, "Dashboard update should succeed"

    # ========================================================================
    # HEALTH MONITOR TESTS
    # ========================================================================

    def test_health_check_cloud_zone(self):
        """Test cloud zone health check."""
        monitor = HealthMonitor()

        status = monitor.check_service_health('cloud_zone')
        assert status in ['healthy', 'degraded', 'critical'], f"Invalid status: {status}"

    def test_health_check_local_zone(self):
        """Test local zone health check."""
        monitor = HealthMonitor()

        status = monitor.check_service_health('local_zone')
        assert status in ['healthy', 'degraded', 'critical'], f"Invalid status: {status}"

    def test_health_check_zone_sync(self):
        """Test zone sync health check."""
        monitor = HealthMonitor()

        status = monitor.check_service_health('zone_sync')
        assert status in ['healthy', 'degraded', 'critical'], f"Invalid status: {status}"

    def test_health_summary(self):
        """Test health summary generation."""
        monitor = HealthMonitor()

        summary = monitor.get_health_summary()
        assert 'overall' in summary, "Summary should have overall status"
        assert isinstance(summary['overall'], str), "Overall status should be string"

    # ========================================================================
    # AUDIT LOG TESTS
    # ========================================================================

    def test_audit_log_creation(self):
        """Test audit log creation."""
        logger = AuditLogger()

        logger.log_action(
            action='test_action',
            actor='test_actor',
            task_id='test_task',
            success=True,
            details={'test': 'data'}
        )

        # Verify log was created
        assert logger.audit_log.exists(), "Audit log file should be created"

    def test_audit_log_format(self):
        """Test audit log format."""
        logger = AuditLogger()

        logger.log_action(
            action='test_action',
            actor='test_actor',
            task_id='test_task',
            success=True,
            details={'test': 'data'}
        )

        # Read log and verify format
        with open(logger.audit_log, 'r') as f:
            log_entry = json.loads(f.readline())

        assert 'timestamp' in log_entry, "Log should have timestamp"
        assert 'action' in log_entry, "Log should have action"
        assert 'actor' in log_entry, "Log should have actor"
        assert log_entry['action'] == 'test_action', "Action should match"

    # ========================================================================
    # INTEGRATION TESTS
    # ========================================================================

    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        print("\n  Testing complete workflow...")

        # 1. Cloud zone creates task
        cloud_manager = CloudZoneManager()
        task_path = cloud_manager.cloud_vault / 'e2e_task.md'
        task_path.write_text("# E2E Test Task\n\n**Type**: draft\n**Priority**: medium")

        # 2. Cloud zone drafts response
        draft_path = cloud_manager.draft_content_in_cloud('linkedin', 'E2E test content')
        assert draft_path.exists(), "Draft should be created"

        # 3. Sync to local zone
        sync_manager = ZoneSyncManager()
        result = sync_manager.sync_file(draft_path, sync_manager.LOCAL_ZONE)
        assert result is True, "Draft should sync to local zone"

        # 4. Local zone processes
        local_manager = LocalZoneManager()
        local_task = sync_manager.LOCAL_ZONE / draft_path.name
        result = local_manager.process_task(local_task)
        assert result is not None, "Local zone should process task"

        print(f"    {Colors.GREEN}✓{Colors.END} Complete workflow successful")

    # ========================================================================
    # RUN ALL TESTS
    # ========================================================================

    def run_all_tests(self):
        """Run all tests."""
        print(f"\n{Colors.BOLD}{'='*70}")
        print(f"AI Employee Vault - Comprehensive Test Suite")
        print(f"{'='*70}{Colors.END}\n")

        self.setup()

        try:
            # Cloud Zone Tests
            print(f"\n{Colors.BOLD}Cloud Zone Tests{Colors.END}")
            print(f"{'-'*70}")
            self.run_test("Cloud Zone Initialization", self.test_cloud_zone_initialization)
            self.run_test("Cloud Can Handle Safe Tasks", self.test_cloud_can_handle_safe_tasks)
            self.run_test("Cloud Blocks Sensitive Tasks", self.test_cloud_blocks_sensitive_tasks)
            self.run_test("Cloud Draft Creation", self.test_cloud_draft_creation)
            self.run_test("Cloud Triage", self.test_cloud_triage)

            # Local Zone Tests
            print(f"\n{Colors.BOLD}Local Zone Tests{Colors.END}")
            print(f"{'-'*70}")
            self.run_test("Local Zone Initialization", self.test_local_zone_initialization)
            self.run_test("Approval Threshold Enforcement", self.test_approval_threshold_enforcement)
            self.run_test("Approval Workflow", self.test_approval_workflow)

            # Zone Sync Tests
            print(f"\n{Colors.BOLD}Zone Sync Tests{Colors.END}")
            print(f"{'-'*70}")
            self.run_test("Claim-by-Move", self.test_claim_by_move)
            self.run_test("Markdown-Only Sync", self.test_markdown_only_sync)
            self.run_test("Secret Filtering", self.test_secret_filtering)
            self.run_test("File Size Limits", self.test_file_size_limits)
            self.run_test("Single-Writer Dashboard", self.test_single_writer_dashboard)

            # Health Monitor Tests
            print(f"\n{Colors.BOLD}Health Monitor Tests{Colors.END}")
            print(f"{'-'*70}")
            self.run_test("Health Check Cloud Zone", self.test_health_check_cloud_zone)
            self.run_test("Health Check Local Zone", self.test_health_check_local_zone)
            self.run_test("Health Check Zone Sync", self.test_health_check_zone_sync)
            self.run_test("Health Summary", self.test_health_summary)

            # Audit Log Tests
            print(f"\n{Colors.BOLD}Audit Log Tests{Colors.END}")
            print(f"{'-'*70}")
            self.run_test("Audit Log Creation", self.test_audit_log_creation)
            self.run_test("Audit Log Format", self.test_audit_log_format)

            # Integration Tests
            print(f"\n{Colors.BOLD}Integration Tests{Colors.END}")
            print(f"{'-'*70}")
            self.run_test("End-to-End Workflow", self.test_end_to_end_workflow)

        finally:
            self.teardown()
            self.results.print_summary()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee Vault Test Suite')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--component', metavar='COMPONENT',
                       help='Test specific component (cloud_zone, local_zone, zone_sync, health_monitor, audit)')
    parser.add_argument('--test', metavar='TEST_NAME',
                       help='Run specific test')
    args = parser.parse_args()

    suite = TestSuite()

    if args.all or not any([args.component, args.test]):
        suite.run_all_tests()
    elif args.component:
        # Run component-specific tests
        suite.setup()
        try:
            if args.component == 'cloud_zone':
                suite.run_test("Cloud Zone Initialization", suite.test_cloud_zone_initialization)
                suite.run_test("Cloud Can Handle Safe Tasks", suite.test_cloud_can_handle_safe_tasks)
                suite.run_test("Cloud Blocks Sensitive Tasks", suite.test_cloud_blocks_sensitive_tasks)
            elif args.component == 'local_zone':
                suite.run_test("Local Zone Initialization", suite.test_local_zone_initialization)
                suite.run_test("Approval Threshold Enforcement", suite.test_approval_threshold_enforcement)
            elif args.component == 'zone_sync':
                suite.run_test("Claim-by-Move", suite.test_claim_by_move)
                suite.run_test("Markdown-Only Sync", suite.test_markdown_only_sync)
                suite.run_test("Secret Filtering", suite.test_secret_filtering)
            elif args.component == 'health_monitor':
                suite.run_test("Health Check Cloud Zone", suite.test_health_check_cloud_zone)
                suite.run_test("Health Summary", suite.test_health_summary)
            elif args.component == 'audit':
                suite.run_test("Audit Log Creation", suite.test_audit_log_creation)
                suite.run_test("Audit Log Format", suite.test_audit_log_format)
        finally:
            suite.teardown()
            suite.results.print_summary()
    elif args.test:
        # Run specific test
        test_method = getattr(suite, args.test, None)
        if test_method:
            suite.setup()
            try:
                suite.run_test(args.test, test_method)
            finally:
                suite.teardown()
                suite.results.print_summary()
        else:
            print(f"[ERROR] Test not found: {args.test}")


if __name__ == '__main__':
    main()
