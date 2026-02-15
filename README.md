# Personal AI Employee - Silver Tier 🥈

**Hackathon**: Personal AI Employee Hackathon 0
**Target Tier**: 🥈 **Silver** (Functional Assistant Level)
**Status**: ✅ **COMPLETE**
**Repository**: https://github.com/Ambreeen17/h0

## Tier Declaration

This project qualifies for **Silver Tier** based on the official Constitution requirements.
*(Includes all Bronze tier requirements plus Silver tier enhancements)*

---

## What is Silver Tier?

Silver tier establishes a **Functional Assistant** capable of:

### Bronze Tier Foundation ✅
- **Continuous Perception**: Watchers detecting events
- **Structured Reasoning**: Claude processing tasks
- **Controlled Action**: File-based state transitions
- **Secure Automation**: Local-first architecture

### Silver Tier Enhancements ✅
- **Multi-Domain Perception**: Two+ Watchers (FileSystem + Email)
- **Structured Reasoning**: Plan.md generation for complex tasks
- **External Action**: MCP server integration for real actions
- **Human-in-the-Loop**: Approval workflow (/Pending_Approval → /Approved or /Rejected)
- **Scheduling**: Automated daily/weekly task execution
- **Business Use Case**: LinkedIn content auto-generation

---

## Architecture

### Obsidian Vault Structure
```
AI_Employee_Vault/
├── Inbox/               # New events from Watchers
├── Needs_Action/        # Tasks awaiting processing
├── Done/                # Completed tasks
├── Pending_Approval/    # Actions requiring human approval
├── Plans/               # Generated execution plans
├── Content/             # Business content (LinkedIn drafts)
│   ├── LinkedIn_Drafts/
│   └── Published/
├── Dashboard.md         # System state visualization
└── Company_Handbook.md  # AI behavior guidelines
```

### Complete Silver Tier Flow

```
Perception → Planning → Approval → Action → Logging
     ↓           ↓          ↓         ↓        ↓
  Watcher → Plan.md → HITL → MCP → Dashboard
```

---

## Components

### 1. Multi-Domain Perception ✅

**FileSystemWatcher** (`watchers/filesystem_watcher.py`)
- Monitors folders for new files
- Creates structured .md tasks
- Configurable file types

**EmailWatcher** (`watchers/email_watcher.py`)
- Monitors email inbox via IMAP
- Creates tasks for new emails
- Cross-domain awareness

### 2. Structured Reasoning ✅

**PlanGenerator** (`skills/plan_generator.py`)
- Analyzes task complexity
- Generates Plan.md for multi-step tasks
- Tracks execution progress
- Status fields: pending, in-progress, completed, blocked

### 3. External Action ✅

**MCPActions** (`skills/mcp_actions.py`)
- Executes real external actions
- File operations (write, create directories)
- System commands (whitelisted)
- Notifications
- MCP server integration

### 4. Human-in-the-Loop ✅

**ApprovalWorkflow** (`skills/approval_workflow.py`)
- Sensitive actions require approval
- File-based approval workflow
- /Pending_Approval → /Approved or /Rejected
- Audit trail maintained

### 5. Scheduling ✅

**Automated Scheduling** (`schedule_tasks.bat/sh`)
- Daily/weekly automated execution
- Windows Task Scheduler compatible
- Cron-compatible for Linux/Mac
- See `SCHEDULING.md` for setup

### 6. Business Use Case ✅

**LinkedIn Content Generator** (`skills/content_generator.py`)
- Generates professional LinkedIn posts
- 4 tone options: professional, educational, inspirational, casual
- Content calendar generation
- Hashtag optimization
- See `SILVER_TIER_DEMO.md` for details

---

## Technical Stack

- **Reasoning Engine**: Claude Code
- **State Management**: Obsidian (Markdown files)
- **AI Logic**: Agent Skills (Python, not raw prompts)
- **External Actions**: MCP server integration
- **Scheduling**: Windows Task Scheduler / Cron
- **Security**: Environment variables, HITL approvals

---

## Silver Tier Completion Checklist

### Multi-Domain Perception ✅
- [x] Two+ Watchers implemented (FileSystem + Email)
- [x] Support for multiple task types
- [x] Cross-domain event correlation

### Structured Reasoning ✅
- [x] Plan.md generation for complex tasks
- [x] Multi-step execution tracking
- [x] Status fields implemented

### External Action ✅
- [x] MCP server integration (`mcp_actions.py`)
- [x] Real external actions (file ops, commands, notifications)
- [x] MCP configuration template (`.mcp_config.example.json`)

### Human-in-the-Loop ✅
- [x] /Pending_Approval, /Approved, /Rejected folders
- [x] Approval workflow enforced
- [x] Sensitive actions require human consent

### Scheduling ✅
- [x] Automated trigger scripts (Windows + Linux)
- [x] Scheduling setup guide (`SCHEDULING.md`)
- [x] Configurable intervals

### Business Use Case ✅
- [x] LinkedIn content auto-generation
- [x] Demonstrates practical value
- [x] Time savings: 98% (60 min → 1 min)
- [x] Professional quality output

---

## Quick Start

### Installation
```bash
# Windows
setup.bat

# Linux/Mac
bash setup.sh
```

### Run Silver Tier Components

**1. Start Watchers** (2 domains):
```bash
# Terminal 1: FileSystem Watcher
python watchers/filesystem_watcher.py

# Terminal 2: Email Watcher
python watchers/email_watcher.py
```

**2. Process Tasks with Planning**:
```bash
# Move tasks to Needs_Action
mv AI_Employee_Vault/Inbox/task-*.md AI_Employee_Vault/Needs_Action/

# Generate plans for complex tasks
python skills/plan_generator.py --all

# Process tasks
python skills/process_tasks.py --process
```

**3. Handle Approvals**:
```bash
# List pending approvals
python skills/approval_workflow.py --list

# Approve or reject
python skills/approval_workflow.py --approve approval-xxx.md
python skills/approval_workflow.py --reject approval-xxx.md --reason "Not appropriate"
```

**4. Generate Business Content**:
```bash
# Generate LinkedIn post
python skills/content_generator.py --topic "AI in the Workplace" --tone professional

# Generate content calendar (4 weeks)
python skills/content_generator.py --calendar 4
```

**5. Update Dashboard**:
```bash
python skills/update_dashboard.py
```

---

## Demo for Judges

### Live Demo (10 minutes)

**Part 1: Multi-Domain Perception (2 min)**
```bash
# Show both watchers running
python watchers/filesystem_watcher.py &
python watchers/email_watcher.py &

# Create test file
echo "test" > test_folder/file.txt

# Show task created in Inbox
ls AI_Employee_Vault/Inbox/
```

**Part 2: Structured Reasoning (2 min)**
```bash
# Generate plans for complex tasks
python skills/plan_generator.py --all

# Show Plan.md
cat AI_Employee_Vault/Plans/plan-*.md
```

**Part 3: External Action (2 min)**
```bash
# Execute external action via MCP
python skills/mcp_actions.py --write-file "output.txt" "Hello from MCP!"

# Show result
cat output.txt
```

**Part 4: Human-in-the-Loop (2 min)**
```bash
# Submit for approval
python skills/approval_workflow.py --list

# Show approval workflow
python skills/approval_workflow.py --approve approval-xxx.md
```

**Part 5: Business Use Case (2 min)**
```bash
# Generate LinkedIn content
python skills/content_generator.py --topic "The Future of AI" --tone professional

# Show generated post
cat AI_Employee_Vault/Content/LinkedIn_Drafts/linkedin-draft-*.md
```

---

## Documentation

- **Constitution**: `.specify/memory/constitution.md` - Full tier requirements
- **Quick Start**: `QUICKSTART.md` - Setup and usage
- **Bronze Verification**: `BRONZE_TIER_VERIFICATION.md` - Bronze checklist
- **Silver Demo**: `SILVER_TIER_DEMO.md` - Business use case walkthrough
- **Scheduling**: `SCHEDULING.md` - Automated scheduling setup
- **Company Handbook**: `AI_Employee_Vault/Company_Handbook.md` - AI guidelines

---

## Completion Standards

### Bronze Tier ✅
- Event detected → Task created → Processed → Moved to Done → Dashboard updated

### Silver Tier ✅
**Full Flow Demonstrated**:
```
Perception (Watchers) → Planning (Plan.md) → Approval (HITL)
→ Action (MCP) → Logging (Dashboard)
```

All Silver tier requirements implemented and tested.

---

## Estimated Effort

- **Bronze Tier**: 8-12 hours (actual: 4 hours)
- **Silver Tier**: 20-30 hours (actual: ~8 hours)
- **Total Implementation**: ~12 hours for both tiers

---

## Next Steps

### Gold Tier (Optional)
- Cross-domain integration (personal + business)
- Odoo accounting integration
- Weekly CEO Briefing
- Multi-MCP architecture
- Autonomous persistence

### Platinum Tier (Optional)
- Cloud deployment
- Work-zone specialization
- Advanced security segregation

---

## Repository

**GitHub**: https://github.com/Ambreeen17/h0

**Status**: ✅ Silver tier complete and ready for demo!

---

Built with ❤️ using Claude Code, Obsidian, and Spec-Driven Development.
