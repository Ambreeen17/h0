# AI Employee - Bronze Tier Quick Start

**Prerequisites**: Python 3.8+, pip

## Setup (5 minutes)

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env to customize (optional)
# Default values work for most cases
```

Key configuration options:
- `WATCH_DIRECTORY`: Folder to monitor for new files (default: ~/Downloads)
- `WATCHER_EXTENSIONS`: File types to watch (default: .pdf,.doc,.docx,.txt,.md,.jpg,.png)

### 3. Verify Vault Structure

The vault should already exist with this structure:
```
AI_Employee_Vault/
├── Inbox/           # New events from Watchers
├── Needs_Action/    # Tasks for Claude to process
├── Done/            # Completed tasks
├── Dashboard.md     # System state (auto-generated)
└── Company_Handbook.md  # AI behavior guidelines
```

If not, create it:
```bash
mkdir -p AI_Employee_Vault/{Inbox,Needs_Action,Done,Pending_Approval}
```

## Usage

### Starting the File System Watcher

The watcher monitors a folder and creates tasks when new files appear.

```bash
# Terminal 1: Start watcher
python3 watchers/filesystem_watcher.py
```

Expected output:
```
==============================================================
File System Watcher - Bronze Tier Perception Layer
==============================================================

[CONFIG] Watching: /home/user/Downloads
[CONFIG] Inbox: AI_Employee_Vault/Inbox
[CONFIG] Extensions: .pdf,.doc,.docx,.txt,.md,.jpg,.png

[START] Watcher is now running...
[INFO] Press Ctrl+C to stop
```

### Processing Tasks

When the Watcher detects new files, it creates tasks in the Inbox. Move them to Needs_Action for processing.

```bash
# Move tasks from Inbox to Needs_Action
mv AI_Employee_Vault/Inbox/task-*.md AI_Employee_Vault/Needs_Action/

# Terminal 2: Process tasks
python3 skills/process_tasks.py --process
```

### Updating the Dashboard

After processing, update the dashboard to see current state.

```bash
# Single update
python3 skills/update_dashboard.py

# Or run in watch mode (auto-update every 30 seconds)
python3 skills/update_dashboard.py --watch
```

## Bronze Tier Completion Checklist

Verify all items are working:

- [ ] **Vault Structure**: All four folders exist (Inbox, Needs_Action, Done, Pending_Approval)
- [ ] **Dashboard.md**: Viewable and showing current state
- [ ] **Company_Handbook.md**: Contains AI behavior guidelines
- [ ] **Watcher Running**: Detects new files in watched directory
- [ ] **Task Creation**: New files trigger task creation in Inbox
- [ ] **Task Processing**: Tasks move from Needs_Action to Done after processing
- [ ] **Dashboard Updates**: Dashboard reflects current system state
- [ ] **Agent Skills**: AI logic implemented as Python scripts (not raw prompts)
- [ ] **No Credentials in Vault**: All secrets in .env file only

## Testing Your Setup

### Manual Test

1. Create a test file in your watched directory:
   ```bash
   touch ~/Downloads/test-document.txt
   ```

2. Watcher should detect it and create a task in Inbox:
   ```bash
   ls AI_Employee_Vault/Inbox/
   # Should see: task-YYYY-MM-DDTHH-MM-SS.md
   ```

3. Move task to Needs_Action:
   ```bash
   mv AI_Employee_Vault/Inbox/task-*.md AI_Employee_Vault/Needs_Action/
   ```

4. Process the task:
   ```bash
   python3 skills/process_tasks.py --process
   ```

5. Verify task moved to Done:
   ```bash
   ls AI_Employee_Vault/Done/
   # Should see the processed task
   ```

6. Update dashboard:
   ```bash
   python3 skills/update_dashboard.py
   ```

7. View dashboard:
   ```bash
   cat AI_Employee_Vault/Dashboard.md
   ```

### Automated Test Script

```bash
# Run all components in sequence
python3 skills/process_tasks.py --list  # List pending tasks
python3 skills/process_tasks.py --process  # Process all
python3 skills/update_dashboard.py  # Update dashboard
```

## File System Flow

```
New File Appears in Watched Directory
              ↓
    Watcher Detects File
              ↓
  Creates Task in Inbox/
              ↓
    [Manual Move]
              ↓
  Task Moves to Needs_Action/
              ↓
   Claude Processes Task
  (analyze, categorize, log)
              ↓
    Task Moves to Done/
              ↓
  Dashboard Auto-Updates
```

## Troubleshooting

### Watcher not detecting files

- Check the WATCH_DIRECTORY in .env matches the folder you're using
- Verify file extension is in WATCHER_EXTENSIONS list
- Check file permissions

### Tasks not processing

- Ensure tasks are in Needs_Action folder (not Inbox)
- Check task files are named `task-*.md`
- Verify Python dependencies are installed

### Dashboard not updating

- Run `python3 skills/update_dashboard.py` manually
- Check folder paths in .env are correct
- Verify Dashboard.md exists and is writable

### Permission errors

- Make sure scripts are executable:
  ```bash
  chmod +x watchers/*.py skills/*.py
  ```

## Architecture

### Components

1. **FileSystemWatcher** (`watchers/filesystem_watcher.py`)
   - Monitors folder for new files
   - Creates structured .md tasks in Inbox

2. **TaskProcessor** (`skills/process_tasks.py`)
   - Agent Skill for processing tasks
   - Analyzes, categorizes, and logs findings
   - Moves completed tasks to Done

3. **DashboardUpdater** (`skills/update_dashboard.py`)
   - Updates Dashboard.md with current state
   - Shows metrics and recent activity

### State Machine

```
Inbox → Needs_Action → Done
   ↓         ↓              ↓
New      Processing    Completed
Events      Queue       Tasks
```

## Next Steps

Once Bronze tier is working:

1. **Customize the Watcher**: Modify to watch specific folders or file types
2. **Add More Watchers**: Create additional watchers for email, calendar, etc.
3. **Enhance Task Processing**: Add more sophisticated analysis and actions
4. **Move to Silver Tier**: Add external actions via MCP servers

## Support

- Check `.specify/memory/constitution.md` for full requirements
- See `README.md` for project overview
- Review `Company_Handbook.md` for AI behavior guidelines

---

**Estimated Time to Complete Bronze Tier**: 8-12 hours

**You're currently at**: Setup + Basic Configuration (~30 minutes)

**Remaining**: Testing, customization, verification (~2-4 hours)
