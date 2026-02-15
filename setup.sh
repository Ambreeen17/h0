#!/bin/bash
# AI Employee - Bronze Tier Setup Script
# This script sets up the environment for the Bronze tier implementation

set -e  # Exit on error

echo "=========================================="
echo "AI Employee - Bronze Tier Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "ERROR: Python 3.8 or higher is required"
    exit 1
fi

echo "✓ Python version OK"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Create environment file
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env

    # Set default paths
    WATCH_DIR="$HOME/Downloads"
    VAULT_DIR="$(pwd)/AI_Employee_Vault"

    echo "Setting default configuration..."
    echo "WATCH_DIRECTORY=$WATCH_DIR" >> .env
    echo "VAULT_INBOX=$VAULT_DIR/Inbox" >> .env
    echo "VAULT_NEEDS_ACTION=$VAULT_DIR/Needs_Action" >> .env
    echo "VAULT_DONE=$VAULT_DIR/Done" >> .env

    echo "✓ .env file created"
else
    echo ".env file already exists, skipping..."
fi
echo ""

# Create vault structure
echo "Creating vault folder structure..."
mkdir -p "$VAULT_DIR/Inbox"
mkdir -p "$VAULT_DIR/Needs_Action"
mkdir -p "$VAULT_DIR/Done"
mkdir -p "$VAULT_DIR/Pending_Approval"

echo "✓ Vault structure created at $VAULT_DIR"
echo ""

# Make scripts executable
echo "Making scripts executable..."
chmod +x watchers/*.py
chmod +x skills/*.py

echo "✓ Scripts made executable"
echo ""

# Create test file to verify setup
echo "Creating test task..."
test_file="$VAULT_DIR/Inbox/task-test-$(date +%s).md"
cat > "$test_file" << 'EOF'
# Test Task

**Created**: 2026-02-15T12:00:00Z
**Status**: pending
**Type**: system-task
**Source**: Setup Script

## Description

This is a test task to verify the AI Employee system is working correctly.

## Processing

### AI Analysis
Test task for verification purposes.

### Actions Taken
- Created test task
- Verified folder structure
- Confirmed setup complete

### Result
System setup verified successfully.

**Completed**: N/A
EOF

echo "✓ Test task created at $test_file"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Review and customize .env file"
echo "2. Start the file system watcher:"
echo "   source venv/bin/activate"
echo "   python3 watchers/filesystem_watcher.py"
echo ""
echo "3. In another terminal, process tasks:"
echo "   source venv/bin/activate"
echo "   python3 skills/process_tasks.py --process"
echo ""
echo "4. Update dashboard:"
echo "   source venv/bin/activate"
echo "   python3 skills/update_dashboard.py"
echo ""
echo "For more information, see QUICKSTART.md"
echo ""
