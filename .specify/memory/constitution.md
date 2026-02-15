<!--
Sync Impact Report:
Version change: Initial → 1.0.0
Added sections:
- Article I: Purpose (Digital FTE framework)
- Article II: General Requirements (all tiers)
- Article III: Bronze Tier (Foundation Level)
- Article IV: Silver Tier (Functional Assistant)
- Article V: Gold Tier (Autonomous Employee)
- Article VI: Platinum Tier (Production Hybrid)
- Article VII: Security & Ethics (mandatory)
- Article VIII: Tier Declaration
- Governance section with versioning

Templates requiring updates:
- ✅ plan-template.md - Constitution Check section will auto-align
- ✅ spec-template.md - No changes needed, template is generic
- ✅ tasks-template.md - No changes needed, template is generic
- ⚠ README.md - Does not exist, should be created with tier declaration
- ⚠ docs/ - Does not exist, consider creating for project documentation

Follow-up TODOs:
- Create README.md declaring target tier (Bronze/Silver/Gold/Platinum)
- Consider creating quickstart.md in docs/ for onboarding
-->

# Personal AI Employee Hackathon 0 Constitution

## Core Principles

### I. Spec-Driven Development (SDD)

All features MUST follow the Spec-Driven Development methodology:
- Every feature starts with a specification (`spec.md`) capturing user stories and requirements
- Architecture decisions documented in `plan.md` before implementation
- Implementation tasks derived from specification in `tasks.md`
- Prompt History Records (PHRs) created for every user interaction
- Architectural Decision Records (ADRs) for significant technical decisions

**Rationale**: SDD ensures traceability from business intent to implementation, enables independent testing of user stories, and maintains auditability for autonomous AI systems.

### II. Local-First Architecture

All Digital FTE implementations MUST be local-first:
- Obsidian vault serves as the system of record for AI state
- File-based state transitions (Inbox → Needs_Action → Done)
- No external dependencies for core reasoning logic
- Credentials stored in environment variables, never in vault
- Human-in-the-loop for sensitive actions

**Rationale**: Local-first ensures data sovereignty, enables offline operation, provides auditability through file system, and maintains human control over autonomous actions.

### III. Tier-Based Progression

All implementations MUST clearly declare their target tier and meet ALL requirements for that tier:
- **Bronze**: Reactive Local Agent (perception → processing → state update)
- **Silver**: Functional Assistant (multi-domain perception + external action + HITL)
- **Gold**: Autonomous Employee (cross-domain + accounting + CEO briefing)
- **Platinum**: Production Hybrid (cloud deployment + work-zone specialization)

Each tier builds upon previous tiers. Tier achievement is binary—either ALL requirements are met or the tier is not achieved.

**Rationale**: Tier-based progression ensures structured growth, enables fair judging across complexity levels, and provides clear milestones for incremental development.

### IV. Agent Skills Over Raw Prompts

All AI automation logic MUST be implemented as Agent Skills:
- No raw prompt-only automation for production workflows
- Skills encapsulate reusable AI capabilities
- Skills version-controlled and testable
- Skills document their contracts (inputs, outputs, side effects)

**Rationale**: Agent Skills provide reproducibility, testability, and composability. Raw prompts are fragile and difficult to maintain at scale.

### V. Human-in-the-Loop (HITL) Mandate

All tiers MUST implement human oversight for sensitive actions:
- File-based approval workflow (/Pending_Approval → /Approved or /Rejected)
- Sensitive operations require explicit human consent
- Audit trail maintained for all autonomous actions
- Kill switches and guardrails for automated processes

**Rationale**: HITL ensures human accountability, provides safety boundaries for autonomous systems, and enables trust in AI decision-making.

### VI. Observability and Auditability

All Digital FTE implementations MUST provide comprehensive visibility:
- JSON audit logs for all autonomous actions
- Structured logging for Watcher events
- State transitions visible through file system
- Dashboard.md reflecting current system state
- Plan.md tracking multi-step execution progress

**Rationale**: Observability is essential for debugging autonomous systems, maintaining trust, and providing judges with verifiable evidence of functionality.

## Tier-Specific Requirements

### Bronze Tier: Foundation Level

**Architecture Requirements**:
- Obsidian Vault (`AI_Employee_Vault`) with folders: /Inbox, /Needs_Action, /Done
- Dashboard.md for system state visualization
- Company_Handbook.md for AI behavior guidelines
- At least one working Watcher (perception layer)

**Functional Requirements**:
- Watcher generates structured .md tasks
- Claude reads /Needs_Action folder
- Claude processes tasks autonomously
- Files move to /Done upon completion
- Dashboard updates to reflect state changes

**Engineering Requirements**:
- AI logic implemented as Agent Skills
- No credentials stored in vault
- Environment variables for all secrets

**Completion Standard**: A detected event automatically creates task → processes → moves to /Done → updates system state.

### Silver Tier: Functional Assistant

**Includes Bronze requirements PLUS**:

**Multi-Domain Perception**:
- Two or more working Watchers
- Support for multiple task types
- Cross-domain event correlation

**Structured Reasoning**:
- Claude generates Plan.md for complex tasks
- Multi-step execution tracking
- Status fields implemented (pending, in-progress, completed, blocked)

**External Action**:
- At least one working MCP server
- Claude performs real external actions (API calls, file operations, etc.)

**Human-in-the-Loop**:
- /Pending_Approval, /Approved, /Rejected folders
- Sensitive actions require file-based approval
- Approval workflow enforced

**Scheduling**:
- Daily or weekly automated trigger
- Demonstrated scheduled task execution

**Business Use Case**:
- LinkedIn content auto-generation OR equivalent business/revenue use case

**Completion Standard**: System demonstrates Perception → Plan → Approval → Action → Logging flow.

### Gold Tier: Autonomous Employee

**Includes Silver requirements PLUS**:

**Cross-Domain Integration**:
- Personal + Business automation unified in single system
- Shared reasoning across domains

**Accounting Integration**:
- Odoo Community deployed (version 19+)
- JSON-RPC integration via MCP
- Financial data flows into CEO briefing

**Multi-MCP Architecture**:
- Separate MCP servers for different capabilities
- Modular external action system

**Weekly CEO Briefing**:
- Automated report including:
  - Revenue summary
  - Bottlenecks and issues
  - Subscription audit
  - Proactive suggestions

**Autonomous Persistence**:
- Ralph Wiggum loop implemented (multi-step completion detection)
- Retry logic for transient failures
- Watchdog or process manager for monitoring

**Reliability & Logging**:
- JSON audit logs for all actions
- Graceful degradation on failures

**Completion Standard**: System demonstrates autonomous, structured business reasoning and controlled action with CEO-level reporting.

### Platinum Tier: Production Hybrid AI Employee

**Includes Gold requirements PLUS**:

**Always-On Cloud Deployment**:
- VM deployment (Oracle/AWS/etc.)
- Persistent Watchers running 24/7
- Health monitoring and alerting

**Work-Zone Specialization**:
- Cloud: drafting + triage (non-sensitive operations)
- Local: approvals + sensitive execution (security boundary)

**Delegation Architecture**:
- Claim-by-move rule: agents claim tasks by moving files
- Single-writer Dashboard rule: only one writer at a time
- Markdown-only sync: no binary files synced between zones

**Security Segregation**:
- Secrets never synced between cloud and local
- Banking operations local-only
- Approval thresholds enforced (e.g., >$100 requires local approval)

**Platinum Demo Gate**:
Demonstration must show:
1. Email arrives while Local zone is offline
2. Cloud zone drafts response
3. Local zone comes online, reviews draft
4. Local zone approves
5. Action executed
6. Logged and archived

**Completion Standard**: Production-capable, secure, fault-tolerant AI Employee system with clear security boundaries between zones.

## Security and Ethics (All Tiers)

**Mandatory Requirements**:
- Use environment variables for ALL credentials
- Never store secrets in Obsidian vault
- Implement HITL for sensitive actions (email sending, money transfers, data deletion)
- Maintain comprehensive audit logs
- Respect automation boundaries (no autonomous actions without approval)
- Retain human accountability for all decisions

**Data Handling**:
- User data remains local unless explicitly approved
- No telemetry or data exfiltration without consent
- Compliance with data protection regulations

## Judging Criteria

All submissions are evaluated on:

| Criteria | Weight | Description |
|----------|--------|-------------|
| Functionality | 30% | Does it work? All requirements met for declared tier? |
| Innovation | 25% | Creative use of AI, novel approaches, technical elegance |
| Practicality | 20% | Real-world utility, business value, usability |
| Security | 15% | HITL safeguards, credential handling, audit trails |
| Documentation | 10% | README, demo video, code comments, architecture clarity |

## Governance

**Amendment Process**:
- Constitution changes require explicit version bump (semantic versioning)
- MAJOR version: Backward-incompatible changes (tier removal, principle redefinition)
- MINOR version: New tier added or material expansion of requirements
- PATCH version: Clarifications, wording fixes, non-semantic changes

**Compliance Review**:
- All feature specifications MUST reference applicable constitution principles
- Implementation plans MUST include Constitution Check section
- Tasks MUST verify compliance with tier requirements
- PR reviews MUST validate constitution adherence

**Tier Declaration**:
Each submission MUST clearly declare:
> "This project qualifies for [Bronze / Silver / Gold / Platinum] Tier based on the official Constitution requirements."

Judges will verify deliverables against this constitution. A tier is considered achieved ONLY if:
- All mandatory requirements for that tier are implemented
- Architecture aligns with official specifications
- Demo proves functional flow
- Security and HITL safeguards are operational

**Guidance**:
- See `.specify/memory/constitution.md` for this document
- See `.specify/templates/plan-template.md` for Constitution Check integration
- See individual tier requirements for detailed acceptance criteria

---

**Version**: 1.0.0 | **Ratified**: 2026-02-15 | **Last Amended**: 2026-02-15
