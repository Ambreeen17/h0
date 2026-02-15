---
id: 001
title: Constitution Hackathon 0 Framework
stage: constitution
date: 2026-02-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: User
command: /sp.constitution
labels: ["constitution","hackathon","framework","governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md (created - full constitution with tier-based requirements)
tests:
  - None (constitution update)
---

## Prompt

Personal AI Employee Hackathon 0
Building Autonomous FTEs (Full-Time Equivalent) in 2026
Built using:


Claude Code


Obsidian (Local Vault)


Watchers (Perception Layer)


MCP Servers (Action Layer)


This version is optimized for judges.

🏛 FINAL OFFICIAL TIER CONSTITUTION
Personal AI Employee Hackathon 0

ARTICLE I — PURPOSE
This Hackathon establishes a structured framework for building a Digital FTE (Full-Time Equivalent) — a local-first, agent-driven, human-in-the-loop AI Employee capable of:


Continuous perception


Structured reasoning


Controlled external action


Secure automation


Each tier represents increasing operational maturity and autonomy.

ARTICLE II — GENERAL REQUIREMENTS (ALL TIERS)
All participants must:


Use Claude Code as the primary reasoning engine


Implement AI logic via Agent Skills


Use Obsidian as the system vault


Follow local-first architecture


Implement file-based state transitions


Maintain security best practices


Submit GitHub repo + README + demo video


Judging Weights:


Functionality — 30%


Innovation — 25%


Practicality — 20%


Security — 15%


Documentation — 10%



🥉 ARTICLE III — BRONZE TIER
Foundation Level (Reactive Local Agent)
Required Architecture


Obsidian Vault (AI_Employee_Vault)


Folders:


/Inbox


/Needs_Action


/Done




Dashboard.md


Company_Handbook.md


Functional Requirements


At least one working Watcher


Watcher generates structured .md tasks


Claude reads /Needs_Action


Claude processes tasks


Files move to /Done


Dashboard updates


Engineering Requirements


AI logic implemented as Agent Skills


No raw prompt-only automation


No credentials inside vault


Completion Standard
A detected event automatically:


Creates task


Gets processed


Moves to /Done


Updates system state


Estimated Effort: 8–12 hours

🥈 ARTICLE IV — SILVER TIER
Functional Assistant Level
(Must include Bronze)
Multi-Domain Perception


Two or more working Watchers


Supports multiple task types


Structured Reasoning


Claude generates Plan.md


Multi-step execution tracking


Status fields implemented


External Action


At least one working MCP server


Claude performs real external action


Human-in-the-Loop


/Pending_Approval


/Approved


/Rejected


Sensitive actions require file-based approval


Scheduling


Daily or weekly automated trigger


Demonstrated scheduled task execution


Business Use Case


LinkedIn content auto-generation


Demonstrates business or revenue use


Completion Standard
System demonstrates:
Perception → Plan → Approval → Action → Logging
Estimated Effort: 20–30 hours

🥇 ARTICLE V — GOLD TIER
Autonomous Employee Level
(Must include Silver)
Cross-Domain Integration


Personal + Business automation unified


Accounting Integration


Odoo Community deployed (19+)


JSON-RPC integration via MCP


Multi-MCP Architecture


Separate MCP servers


Modular external action system


Weekly CEO Briefing
Automated report including:


Revenue summary


Bottlenecks


Subscription audit


Proactive suggestions


Autonomous Persistence


Ralph Wiggum loop implemented


Multi-step completion detection


Reliability & Logging


JSON audit logs


Retry logic


Watchdog or process manager


Graceful degradation


Completion Standard
System demonstrates autonomous, structured business reasoning and controlled action.
Estimated Effort: 40+ hours

💎 ARTICLE VI — PLATINUM TIER
Production Hybrid AI Employee
(Must include Gold)
Always-On Cloud Deployment


VM deployment (Oracle/AWS/etc.)


Persistent Watchers


Health monitoring


Work-Zone Specialization


Cloud: drafting + triage


Local: approvals + sensitive execution


Delegation Architecture


Claim-by-move rule


Single-writer Dashboard rule


Markdown-only sync


Security Segregation


Secrets never synced


Banking local-only


Approval thresholds enforced


Platinum Demo Gate
Demonstration must show:


Email arrives while Local offline


Cloud drafts response


Local approves


Action executed


Logged and archived


Completion Standard
Production-capable, secure, fault-tolerant AI Employee system.
Estimated Effort: 60+ hours

ARTICLE VII — SECURITY & ETHICS (MANDATORY ALL TIERS)
Participants must:


Use environment variables for credentials


Never store secrets in vault


Implement HITL for sensitive actions


Maintain audit logs


Respect automation boundaries


Retain human accountability



ARTICLE VIII — TIER DECLARATION
Each submission must clearly declare:

"This project qualifies for [Bronze / Silver / Gold / Platinum] Tier based on the official Constitution requirements."

Judges will verify deliverables against this document.

FINAL DECLARATION
A tier is considered achieved only if:


All mandatory requirements are implemented


Architecture aligns with official specifications


Demo proves functional flow


Security and HITL safeguards are operational


This Constitution governs structured progression from:
Reactive Local Agent → Functional Assistant → Autonomous Employee → Production AI FTE

## Response snapshot

Successfully created the Personal AI Employee Hackathon 0 Constitution at `.specify/memory/constitution.md` with:

- **Version**: 1.0.0 (initial ratification)
- **Core Principles**: SDD, Local-First Architecture, Tier-Based Progression, Agent Skills, HITL Mandate, Observability
- **Tier Requirements**: Complete specifications for Bronze, Silver, Gold, and Platinum tiers
- **Security & Ethics**: Mandatory requirements across all tiers
- **Governance**: Amendment process, compliance review, tier declaration protocol

**Sync Impact Report** generated documenting:
- All new sections added
- Template compatibility verified (plan.md, spec.md, tasks.md templates compatible)
- Follow-up items: README.md creation, docs/ consideration

**Key Decisions**:
- Tier-based binary achievement (all requirements must be met)
- File-based state transitions as primary mechanism
- Agent Skills over raw prompts for maintainability
- HITL mandatory for all sensitive actions
- Observability through file system and audit logs

## Outcome

- ✅ Impact: Established foundational governance document for Hackathon 0, defining tier progression from Bronze (reactive agent) through Platinum (production hybrid system)
- 🧪 Tests: N/A (constitution document)
- 📁 Files: Created `.specify/memory/constitution.md` with complete tier framework, security requirements, judging criteria, and governance model
- 🔁 Next prompts: Consider creating README.md declaring target tier; create feature specs for specific tier implementation
- 🧠 Reflection: Constitution successfully translated user's hackathon requirements into structured governance document with clear acceptance criteria, security boundaries, and compliance gates

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): Create README.md with tier declaration to establish project scope
