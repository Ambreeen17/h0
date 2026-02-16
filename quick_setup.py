#!/usr/bin/env python3
"""
Quick Setup Script - AI Employee Vault
Automatically creates all required directories and verifies setup
"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """Create all required directories for the vault system."""
    print("=" * 70)
    print("AI Employee Vault - Quick Setup")
    print("=" * 70)
    print()

    # Define directories to create
    directories = [
        # Local Zone
        "AI_Employee_Vault/Inbox",
        "AI_Employee_Vault/Needs_Action",
        "AI_Employee_Vault/Done",
        "AI_Employee_Vault/Pending_Approval",
        "AI_Employee_Vault/Approved",
        "AI_Employee_Vault/Rejected",
        "AI_Employee_Vault/Audit",
        "AI_Employee_Vault/CEO_Briefings",
        "AI_Employee_Vault/Content",
        "AI_Employee_Vault/Dashboard",
        "AI_Employee_Vault/Plans",
        "AI_Employee_Vault/Content/LinkedIn_Drafts",

        # Cloud Zone
        "AI_Employee_Vault_Cloud/Inbox",
        "AI_Employee_Vault_Cloud/Needs_Action",
        "AI_Employee_Vault_Cloud/Done",
        "AI_Employee_Vault_Cloud/Drafts",
        "AI_Employee_Vault_Cloud/Triage",

        # Sync
        "zone_sync_queue",
        "local_zone_sync",

        # Logs
        "logs",
    ]

    print("[INFO] Creating directory structure...")
    created = 0
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  [CREATE] {directory}/")
            created += 1
        else:
            print(f"  [EXISTS] {directory}/")

    print(f"\n[OK] Created {created} directories")

def check_env_file():
    """Check if .env file exists."""
    print()
    print("[INFO] Checking environment configuration...")

    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        print("  [EXISTS] .env file found [OK]")
        return True
    elif env_example.exists():
        print("  [COPY] Creating .env from .env.example...")
        import shutil
        shutil.copy(env_example, env_file)
        print("  [OK] .env file created [OK]")
        return True
    else:
        print("  [WARN] .env.example not found")
        print("  [INFO] Creating basic .env file...")

        env_content = """# AI Employee Vault Configuration

# Vault Paths (use default values)
VAULT_INBOX=AI_Employee_Vault/Inbox
VAULT_NEEDS_ACTION=AI_Employee_Vault/Needs_Action
VAULT_DONE=AI_Employee_Vault/Done
VAULT_PENDING_APPROVAL=AI_Employee_Vault/Pending_Approval

# Cloud Zone Paths
CLOUD_VAULT=AI_Employee_Vault_Cloud
LOCAL_VAULT=AI_Employee_Vault

# Watcher Configuration
WATCH_DIRECTORY=./test_watches
WATCHER_EXTENSIONS=.pdf,.doc,.docx,.txt,.md,.jpg,.png

# Logging
LOG_LEVEL=INFO
"""
        env_file.write_text(env_content)
        print("  [OK] Basic .env file created [OK]")
        return True

def verify_python_packages():
    """Check if required Python packages are installed."""
    print()
    print("[INFO] Checking Python packages...")

    required_packages = {
        'watchdog': 'File system watching',
        'dotenv': 'Environment configuration (python-dotenv)',
        'filelock': 'File locking for zones',
    }

    missing = []
    for package, description in required_packages.items():
        try:
            if package == 'dotenv':
                import dotenv
            elif package == 'filelock':
                import filelock
            else:
                __import__(package)
            print(f"  [OK] {package} - {description} [OK]")
        except ImportError:
            print(f"  [MISSING] {package} - {description} [FAIL]")
            missing.append(package)

    if missing:
        print()
        print(f"[WARN] Missing packages: {', '.join(missing)}")
        print("[INFO] Install with: pip install -r requirements.txt")
        return False
    else:
        print()
        print("[OK] All required packages installed [OK]")
        return True

def verify_node_npm():
    """Check if Node.js and npx are available."""
    print()
    print("[INFO] Checking Node.js and npx...")

    # Check Node.js
    node_check = os.system("node --version > nul 2>&1" if os.name == "nt" else "node --version > /dev/null 2>&1")
    if node_check == 0:
        print("  [OK] Node.js installed [OK]")
    else:
        print("  [WARN] Node.js not found (optional for MCP servers)")

    # Check npx
    npx_check = os.system("npx --version > nul 2>&1" if os.name == "nt" else "npx --version > /dev/null 2>&1")
    if npx_check == 0:
        print("  [OK] npx installed [OK]")
    else:
        print("  [WARN] npx not found (optional for MCP servers)")

    return node_check == 0 and npx_check == 0

def create_test_watches():
    """Create a test watches directory for demo."""
    print()
    print("[INFO] Creating test watches directory...")

    test_dir = Path("test_watches")
    test_dir.mkdir(exist_ok=True)

    # Create a README in test watches
    readme = test_dir / "README.md"
    if not readme.exists():
        readme.write_text("""# Test Watches Directory

Drop files here to test the File System Watcher.

Supported formats:
- PDF documents (.pdf)
- Word documents (.doc, .docx)
- Text files (.txt)
- Markdown files (.md)
- Images (.jpg, .png)

The watcher will automatically create tasks in the AI_Employee_Vault/Inbox folder.
""")
        print("  [CREATE] test_watches/README.md")

    print("  [OK] Test watches directory ready [OK]")

def main():
    """Run all setup checks."""
    try:
        # 1. Create directories
        create_directory_structure()

        # 2. Setup environment
        env_ok = check_env_file()

        # 3. Verify packages
        packages_ok = verify_python_packages()

        # 4. Verify Node.js/npx
        node_ok = verify_node_npm()

        # 5. Create test watches
        create_test_watches()

        # Summary
        print()
        print("=" * 70)
        print("SETUP SUMMARY")
        print("=" * 70)
        print()
        print(f"Directory Structure: [OK] READY")
        print(f"Environment File: {'[OK] READY' if env_ok else '[WARN]  CREATED'}")
        print(f"Python Packages: {'[OK] READY' if packages_ok else '[WARN]  NEEDS INSTALL'}")
        print(f"Node.js/npx: {'[OK] READY' if node_ok else '[WARN]  OPTIONAL'}")
        print()

        if packages_ok:
            print("[OK] SYSTEM READY FOR HACKATHON DEMO!")
            print()
            print("Next steps:")
            print("1. Run tests: python tests/test_suite.py --all")
            print("2. Run demo: python skills/cloud_zone_manager.py --status")
            print("3. Follow PLATINUM_DEMO.md for full demo")
        else:
            print("[WARN]  ACTION NEEDED:")
            print("   pip install -r requirements.txt")
            print()
            print("Then run this script again.")

        print()
        print("=" * 70)

    except Exception as e:
        print(f"\n[ERROR] Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
