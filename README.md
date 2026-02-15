# Personal AI Employee - Bronze Tier

**Hackathon**: Personal AI Employee Hackathon 0
**Target Tier**: 🥉 **Bronze** (Foundation Level - Reactive Local Agent)
**Status**: In Development

## Tier Declaration

This project qualifies for **Bronze Tier** based on the official Constitution requirements.

## What is Bronze Tier?

Bronze tier establishes a **Reactive Local Agent** capable of:
- **Continuous Perception**: At least one Watcher detecting events
- **Structured Reasoning**: Claude processing tasks from /Needs_Action
- **Controlled Action**: File-based state transitions (Inbox → Needs_Action → Done)
- **Secure Automation**: Local-first architecture with no credentials in vault

## Architecture

### Obsidian Vault Structure
```
AI_Employee_Vault/
├── Inbox/           # New events detected by Watchers
├── Needs_Action/    # Tasks awaiting Claude processing
├── Done/            # Completed tasks
├── Dashboard.md     # System state visualization
└── Company_Handbook.md  # AI behavior guidelines
```

### Flow
```
Watcher detects event
    ↓
Creates .md task in Inbox
    ↓
Task moves to Needs_Action
    ↓
Claude reads and processes task
    ↓
Task moves to Done
    ↓
Dashboard.md updates
```

## Technical Stack

- **Reasoning Engine**: Claude Code
- **State Management**: Obsidian (Markdown files)
- **AI Logic**: Agent Skills (no raw prompts)
- **Security**: Environment variables for credentials (never in vault)

## Completion Criteria

Bronze tier is achieved when:
- ✅ Obsidian vault with required folders exists
- ✅ At least one Watcher generates structured .md tasks
- ✅ Claude reads /Needs_Action and processes tasks
- ✅ Files move to /Done upon completion
- ✅ Dashboard.md updates to reflect state changes
- ✅ AI logic implemented as Agent Skills
- ✅ No credentials stored in vault

## Estimated Effort

8-12 hours for complete Bronze tier implementation.

## Project Documentation

- **Constitution**: `.specify/memory/constitution.md` - Full tier requirements and governance
- **Feature Specs**: `specs/` - Individual feature specifications
- **Plans**: `specs/*/plan.md` - Architecture decisions
- **Tasks**: `specs/*/tasks.md` - Implementation tasks

## Demo

[Demo video link to be added]

---

Built with ❤️ using Claude Code, Obsidian, and Spec-Driven Development.
