# AI Employee Vault - Architecture Diagrams

**Version**: 1.0.0
**Last Updated**: 2026-02-16
**Tier**: Platinum

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Cloud/Local Zone Architecture](#cloudlocal-zone-architecture)
3. [Data Flow Diagrams](#data-flow-diagrams)
4. [Security Boundaries](#security-boundaries)
5. [MCP Integration Map](#mcp-integration-map)
6. [Deployment Architecture](#deployment-architecture)
7. [State Machine](#state-machine)
8. [Component Interactions](#component-interactions)

---

## System Overview

### High-Level Architecture

```mermaid
graph TB
    subgraph "External Inputs"
        EMAIL[Email Server]
        FILES[File System]
        SCHED[Scheduled Tasks]
        WEB[Webhooks]
    end

    subgraph "Perception Layer (Watchers)"
        EW[EmailWatcher]
        FSW[FileSystemWatcher]
        SW[ScheduledWatcher]
        WW[WebhookWatcher]
    end

    subgraph "Cloud Zone (24/7)"
        CZM[CloudZoneManager]
        DRAFTS[Drafts Folder]
        TRIAGE[Triage Engine]
    end

    subgraph "Zone Sync (Secure)"
        ZSM[ZoneSyncManager]
        LOCK[File Locking]
        FILTER[Secret Filter]
    end

    subgraph "Local Zone (Secure)"
        LZM[LocalZoneManager]
        APPROVAL[Approval Workflow]
        AUDIT[Audit Logger]
    end

    subgraph "Action Layer (MCP)"
        EMAIL_MCP[Email MCP]
        LINKEDIN_MCP[LinkedIn MCP]
        ODOO_MCP[Odoo MCP]
        FILE_MCP[Filesystem MCP]
    end

    subgraph "Observability"
        HM[HealthMonitor]
        DASH[Dashboard]
        LOGS[Audit Logs]
    end

    EMAIL --> EW
    FILES --> FSW
    SCHED --> SW
    WEB --> WW

    EW --> CZM
    FSW --> CZM
    SW --> CZM
    WW --> CZM

    CZM --> DRAFTS
    CZM --> TRIAGE

    DRAFTS --> ZSM
    TRIAGE --> ZSM

    ZSM --> LOCK
    ZSM --> FILTER
    LOCK --> LZM
    FILTER --> LZM

    LZM --> APPROVAL
    APPROVAL --> LZM

    LZM --> EMAIL_MCP
    LZM --> LINKEDIN_MCP
    LZM --> ODOO_MCP
    LZM --> FILE_MCP

    EMAIL_MCP --> AUDIT
    LINKEDIN_MCP --> AUDIT
    ODOO_MCP --> AUDIT
    FILE_MCP --> AUDIT

    AUDIT --> LOGS

    HM --> CZM
    HM --> LZM
    HM --> ZSM

    CZM --> DASH
    LZM --> DASH

    style CZM fill:#e1f5ff
    style LZM fill:#fff4e1
    style ZSM fill:#f0e1ff
    style HM fill:#e1ffe1
```

---

## Cloud/Local Zone Architecture

### Zone Specialization

```mermaid
graph LR
    subgraph "Cloud Zone (Safe Operations)"
        direction TB
        C1[Content Drafting]
        C2[Data Analysis]
        C3[Triage & Classification]
        C4[Plan Generation]
        C5[Pre-Processing]
    end

    subgraph "Local Zone (Secure Operations)"
        direction TB
        L1[Approval Decisions]
        L2[Credential Access]
        L3[Banking Operations]
        L4[Sensitive Execution]
        L5[Final Authorization]
    end

    subgraph "Secure Sync"
        S1[Markdown-Only]
        S2[Secret Filtering]
        S3[File Locking]
    end

    C1 --> S1
    C2 --> S1
    C3 --> S1
    C4 --> S1
    C5 --> S1

    S1 --> S2
    S2 --> S3
    S3 --> L1
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5

    style C1 fill:#e1f5ff
    style C2 fill:#e1f5ff
    style C3 fill:#e1f5ff
    style C4 fill:#e1f5ff
    style C5 fill:#e1f5ff
    style L1 fill:#fff4e1
    style L2 fill:#fff4e1
    style L3 fill:#fff4e1
    style L4 fill:#fff4e1
    style L5 fill:#fff4e1
    style S1 fill:#f0e1ff
    style S2 fill:#ffe1e1
    style S3 fill:#e1ffe1
```

### Zone Communication Flow

```mermaid
sequenceDiagram
    participant E as External Event
    participant CZ as Cloud Zone
    participant ZS as Zone Sync
    participant LZ as Local Zone
    participant H as Human

    E->>CZ: Email arrives
    CZ->>CZ: Detect & analyze
    CZ->>CZ: Draft response
    CZ->>ZS: Prepare for sync
    ZS->>ZS: Filter secrets
    ZS->>LZ: Sync markdown
    LZ->>LZ: Review draft
    LZ->>H: Request approval
    H->>LZ: Approve action
    LZ->>LZ: Execute securely
    LZ->>CZ: Sync confirmation
```

---

## Data Flow Diagrams

### Complete Task Lifecycle

```mermaid
flowchart TD
    START([External Event])

    INBOX[Inbox Folder]
    WATCHER{Watcher Type?}
    NEEDS[Needs_Action Folder]

    CZ{Cloud Zone<br/>Can Handle?}
    DRAFT[Create Draft]
    TRIAGE[Triage Task]

    SYNC{Needs<br/>Local Zone?}
    PREP[Prepare Sync Package]

    FILTER{Secret<br/>Filter}
    BLOCK[Block Sync]
    SYNC_QUEUE[Sync Queue]

    LZ_ARRIVE[Local Zone]
    APPROVAL{Requires<br/>Approval?}

    PENDING[Pending_Approval]
    HUMAN[Human Review]
    APPROVED[Approved Folder]
    REJECTED[Rejected Folder]

    EXECUTE[Execute Action]
    MCP[MCP Server]

    AUDIT[Log to Audit]
    DONE[Done Folder]

    DASH_UPDATE[Update Dashboard]

    START --> INBOX
    INBOX --> WATCHER

    WATCHER -->|Email| EMAIL_T[Email Task]
    WATCHER -->|File| FILE_T[File Task]
    WATCHER -->|Schedule| SCHED_T[Scheduled Task]

    EMAIL_T --> NEEDS
    FILE_T --> NEEDS
    SCHED_T --> NEEDS

    NEEDS --> CZ

    CZ -->|Yes| DRAFT
    CZ -->|No| TRIAGE

    DRAFT --> SYNC
    TRIAGE --> SYNC

    SYNC -->|Yes| PREP
    SYNC -->|No| CZ

    PREP --> FILTER

    FILTER -->|Blocked| BLOCK
    FILTER -->|Passed| SYNC_QUEUE

    SYNC_QUEUE --> LZ_ARRIVE

    LZ_ARRIVE --> APPROVAL

    APPROVAL -->|Yes| PENDING
    APPROVAL -->|No| EXECUTE

    PENDING --> HUMAN

    HUMAN -->|Approve| APPROVED
    HUMAN -->|Reject| REJECTED

    APPROVED --> EXECUTE

    EXECUTE --> MCP

    MCP --> AUDIT

    AUDIT --> DONE

    DONE --> DASH_UPDATE

    style CZ fill:#e1f5ff
    style LZ_ARRIVE fill:#fff4e1
    style FILTER fill:#ffe1e1
    style APPROVAL fill:#fff4e1
    style EXECUTE fill:#e1ffe1
```

### Email Processing Flow

```mermaid
flowchart LR
    EMAIL([Email Arrives])

    DETECT[EmailWatcher<br/>Detects New Email]
    CREATE[Create Task in Inbox]
    MOVE[Move to Needs_Action]

    ANALYZE[Cloud Zone<br/>Analyzes Content]
    CLASSIFY{Classification}

    DRAFT_RESP[Draft Response]
    SYNC_LZ[Sync to Local Zone]
    REQ_APPROV[Request Approval]

    HUMAN[Human Reviews]
    DECISION{Decision}

    SEND[Send Email via MCP]
    LOG[Log to Audit]
    ARCHIVE[Archive to Done]

    EMAIL --> DETECT
    DETECT --> CREATE
    CREATE --> MOVE
    MOVE --> ANALYZE
    ANALYZE --> CLASSIFY

    CLASSIFY -->|Inquiry| DRAFT_RESP
    CLASSIFY -->|Spam| ARCHIVE
    CLASSIFY -->|Complex| REQ_APPROV

    DRAFT_RESP --> SYNC_LZ
    SYNC_LZ --> REQ_APPROV
    REQ_APPROV --> HUMAN

    HUMAN --> DECISION
    DECISION -->|Approve| SEND
    DECISION -->|Reject| ARCHIVE

    SEND --> LOG
    LOG --> ARCHIVE

    style ANALYZE fill:#e1f5ff
    style SYNC_LZ fill:#f0e1ff
    style REQ_APPROV fill:#fff4e1
    style HUMAN fill:#ffe1f0
```

---

## Security Boundaries

### Security Zones

```mermaid
graph TB
    subgraph "Public Internet"
        INTERNET[External Sources]
    end

    subgraph "Cloud Zone (Public Cloud)"
        direction TB
        C_VAULT[Cloud Vault]
        C_DRAFT[Drafts]
        C_TRIAGE[Triage]
        NO_CRED[No Credentials<br/>No Secrets]
    end

    subgraph "Security Boundary"
        FILTER[Secret Filter]
        MD_ONLY[Markdown Only]
        SIZE_LIM[Size Limits]
    end

    subgraph "Local Zone (Private)"
        direction TB
        L_VAULT[Local Vault]
        APPROVAL[Approvals]
        CRED[Credentials<br/>.env File]
        BANKING[Banking Ops]
    end

    subgraph "Audit Trail"
        AUDIT[JSON Logs]
        TRACE[Full Traceability]
    end

    INTERNET -->|HTTPS| C_VAULT
    C_VAULT --> C_DRAFT
    C_VAULT --> C_TRIAGE
    NO_CRED --> C_VAULT

    C_DRAFT --> FILTER
    C_TRIAGE --> FILTER

    FILTER --> MD_ONLY
    MD_ONLY --> SIZE_LIM
    SIZE_LIM --> L_VAULT

    L_VAULT --> APPROVAL
    APPROVAL --> CRED
    APPROVAL --> BANKING

    APPROVAL --> AUDIT
    BANKING --> AUDIT

    CRED -.->|Never Synced| NO_CRED

    style C_VAULT fill:#e1f5ff
    style L_VAULT fill:#fff4e1
    style FILTER fill:#ffe1e1
    style AUDIT fill:#e1ffe1
    style NO_CRED fill:#ffcccc
    style CRED fill:#ccffcc
```

### Approval Thresholds

```mermaid
graph LR
    subgraph "No Approval Required"
        NA1[Content Drafting]
        NA2[Data Analysis]
        NA3[Triage]
    end

    subgraph "Approval Required"
        A1[Email Send<br/>ALL]
        A2[API Calls<br/>ALL]
        A3[Banking<br/>>$0]
        A4[File Delete<br/>>10 files]
        A5[Financial<br/>>$100]
    end

    subgraph "Human Review"
        H[Human Decision]
    end

    subgraph "Outcomes"
        O1[Execute]
        O2[Reject]
    end

    NA1 --> O1
    NA2 --> O1
    NA3 --> O1

    A1 --> H
    A2 --> H
    A3 --> H
    A4 --> H
    A5 --> H

    H -->|Approve| O1
    H -->|Reject| O2

    style NA1 fill:#ccffcc
    style NA2 fill:#ccffcc
    style NA3 fill:#ccffcc
    style A1 fill:#ffcccc
    style A2 fill:#ffcccc
    style A3 fill:#ffcccc
    style A4 fill:#ffcccc
    style A5 fill:#ffcccc
    style H fill:#fff4e1
```

---

## MCP Integration Map

### MCP Server Architecture

```mermaid
graph TB
    subgraph "AI Employee Vault"
        LZM[LocalZoneManager]
        ACTIONS[MCPActions]
    end

    subgraph "MCP Servers"
        EMAIL[Email MCP]
        LINKEDIN[LinkedIn MCP]
        ODOO[Odoo MCP]
        FILE[Filesystem MCP]
        SLACK[Slack MCP]
        CAL[Calendar MCP]
    end

    subgraph "External Services"
        GMAIL[Gmail API]
        LI[LinkedIn API]
        ODOO_DB[Odoo DB<br/>JSON-RPC]
        FS[File System]
        SLACK_API[Slack API]
        CAL_API[Calendar API]
    end

    LZM --> ACTIONS

    ACTIONS --> EMAIL
    ACTIONS --> LINKEDIN
    ACTIONS --> ODOO
    ACTIONS --> FILE
    ACTIONS --> SLACK
    ACTIONS --> CAL

    EMAIL --> GMAIL
    LINKEDIN --> LI
    ODOO --> ODOO_DB
    FILE --> FS
    SLACK --> SLACK_API
    CAL --> CAL_API

    style EMAIL fill:#e1f5ff
    style LINKEDIN fill:#e1f5ff
    style ODOO fill:#e1f5ff
    style FILE fill:#e1f5ff
    style SLACK fill:#e1f5ff
    style CAL fill:#e1f5ff
    style ODOO_DB fill:#fff4e1
```

### MCP Action Flow

```mermaid
sequenceDiagram
    participant LZ as LocalZone
    participant MA as MCPActions
    participant App as Approval
    participant MCP as MCP Server
    participant Ext as External Service

    LZ->>MA: Execute action
    MA->>App: Check approval
    App-->>MA: Approved

    MA->>MCP: Send request
    MCP->>Ext: Call API
    Ext-->>MCP: Result
    MCP-->>MA: Response

    MA->>MA: Log to audit
    MA-->>LZ: Return result

    LZ->>LZ: Update Dashboard
```

---

## Deployment Architecture

### Production Deployment

```mermaid
graph TB
    subgraph "Cloud VM (Oracle/AWS/GCP)"
        direction TB
        CZ_VAULT[AI_Employee_Vault_Cloud]
        CZM[CloudZoneManager]
        ZSM[ZoneSyncManager]
        HM[HealthMonitor]
        WATCHERS[Watchers<br/>24/7]
    end

    subgraph "Local Machine (On-Premise)"
        direction TB
        LZ_VAULT[AI_Employee_Vault]
        LZM[LocalZoneManager]
        APPROVAL[Approval Workflow]
        CRED[Credentials<br/>.env]
        MCP[MCP Servers]
    end

    subgraph "Secure Channel"
        SYNC[Sync Queue<br/>Markdown Only]
        FILTER[Secret Filter]
    end

    subgraph "Monitoring"
        LOGS[Centralized Logs]
        ALERTS[Alerts]
        DASH[Dashboard]
    end

    WATCHERS --> CZM
    CZM --> CZ_VAULT
    CZM --> ZSM
    ZSM --> FILTER
    FILTER --> SYNC
    SYNC --> LZM
    LZM --> LZ_VAULT
    LZM --> APPROVAL
    APPROVAL --> MCP

    HM --> CZM
    HM --> LZM
    HM --> ZSM

    CZM --> LOGS
    LZM --> LOGS
    ZSM --> LOGS

    HM --> ALERTS
    LOGS --> DASH

    CZ_VAULT -.->|No Secrets| LZ_VAULT
    CRED -.->|Never Synced| CZ_VAULT

    style CZ_VAULT fill:#e1f5ff
    style LZ_VAULT fill:#fff4e1
    style SYNC fill:#f0e1ff
    style FILTER fill:#ffe1e1
    style CRED fill:#ccffcc
```

### Development/Simulation Mode

```mermaid
graph LR
    subgraph "Single Machine"
        DEV[Developer Machine]

        subgraph "Local Folders"
            CLOUD[AI_Employee_Vault_Cloud<br/>./cloud_zone]
            LOCAL[AI_Employee_Vault<br/>./local_zone]
            SYNC[zone_sync_queue<br/>./sync_queue]
        end

        subgraph "Processes"
            CZM[CloudZoneManager]
            LZM[LocalZoneManager]
            ZSM[ZoneSyncManager]
            HM[HealthMonitor]
        end
    end

    CZM <---> CLOUD
    LZM <---> LOCAL
    ZSM <---> SYNC

    CZM <-->|Simulated Network| ZSM
    ZSM <-->|Simulated Network| LZM

    HM <--> CZM
    HM <--> LZM
    HM <--> ZSM

    style CLOUD fill:#e1f5ff
    style LOCAL fill:#fff4e1
    style SYNC fill:#f0e1ff
```

---

## State Machine

### Task State Transitions

```mermaid
stateDiagram-v2
    [*] --> Inbox: External Event

    Inbox --> Needs_Action: Watcher Detection
    Needs_Action --> Cloud_Zone: Task Processing

    Cloud_Zone --> Drafting: Can Handle in Cloud
    Cloud_Zone --> Triage: Needs Classification

    Drafting --> Sync_Queue: Draft Complete
    Triage --> Sync_Queue: Classified

    Sync_Queue --> Local_Zone: Secure Sync

    Local_Zone --> Pending_Approval: Requires Approval
    Local_Zone --> Executing: No Approval Needed

    Pending_Approval --> Approved: Human Approves
    Pending_Approval --> Rejected: Human Rejects

    Approved --> Executing: Execute Action

    Executing --> Done: Success
    Executing --> Blocked: Failure

    Blocked --> Pending_Approval: Retry
    Blocked --> Done: Max Retries

    Rejected --> Done: Archived
    Done --> [*]: Complete

    note right of Cloud_Zone
        Safe Operations:
        - Drafting
        - Analysis
        - Triage
    end note

    note right of Local_Zone
        Secure Operations:
        - Approvals
        - Execution
        - Banking
    end note

    note right of Pending_Approval
        Human-in-the-Loop
        Approval Gate
    end note
```

---

## Component Interactions

### Claim-by-Move Delegation

```mermaid
sequenceDiagram
    participant C as Cloud Zone
    participant S as Sync Manager
    participant L as Local Zone
    participant F as File System

    C->>S: Claim task
    S->>S: Create claim file
    S->>F: Move task file
    F-->>S: Move complete
    S-->>C: Claim confirmed

    Note over C,F: Atomic operation<br/>prevents race conditions

    L->>S: Check claim
    S-->>L: Claim details
    L->>F: Read task
    F-->>L: Task content

    L->>L: Process task
    L->>S: Update claim
    S->>S: Mark complete
```

### Single-Writer Dashboard

```mermaid
sequenceDiagram
    participant P1 as Process 1
    participant L as File Lock
    participant D as Dashboard
    participant P2 as Process 2

    P1->>L: Acquire lock
    L-->>P1: Lock granted

    Note over P1,D: Process 1 writing

    P2->>L: Acquire lock
    L-->>P2: Lock timeout

    Note over P2: Process 2 waits

    P1->>D: Write update
    D-->>P1: Write complete
    P1->>L: Release lock

    L-->>P2: Lock granted
    P2->>D: Write update
    D-->>P2: Write complete
    P2->>L: Release lock

    Note over L: Only one writer<br/>at a time
```

### Health Monitoring Loop

```mermaid
graph LR
    START([Start Monitoring])

    CHECK[Check All Services]
    LOG[Log Health Status]
    HEALTHY{All Healthy?}

    ALERT[Log Alert]
    COUNT[Increment Failure Counter]
    THRESHOLD{>= 3 Failures?}

    RECOVER[Attempt Recovery]
    RESET[Reset Counter]

    WAIT[Wait 30 seconds]
    ITERATIONS{More<br/>Iterations?}

    DONE([Monitoring Complete])

    START --> CHECK
    CHECK --> LOG
    LOG --> HEALTHY

    HEALTHY -->|Yes| RESET
    HEALTHY -->|No| ALERT

    ALERT --> COUNT
    COUNT --> THRESHOLD

    THRESHOLD -->|Yes| RECOVER
    THRESHOLD -->|No| WAIT

    RECOVER --> RESET

    RESET --> WAIT
    WAIT --> ITERATIONS

    ITERATIONS -->|Yes| CHECK
    ITERATIONS -->|No| DONE

    style CHECK fill:#e1f5ff
    style ALERT fill:#ffcccc
    style RECOVER fill:#fff4e1
    style RESET fill:#ccffcc
```

---

## ASCII Diagrams

### System Overview (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AI EMPLOYEE VAULT                               │
│                         Platinum Tier Architecture                     │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  EXTERNAL    │      │  CLOUD ZONE  │      │  LOCAL ZONE  │
│   INPUTS     │──────│   (24/7)     │──────│   (Secure)   │
├──────────────┤      ├──────────────┤      ├──────────────┤
│ • Email      │      │ • Drafting   │      │ • Approvals  │
│ • Files      │      │ • Analysis   │      │ • Banking    │
│ • Schedule   │      │ • Triage     │      │ • Execution  │
│ • Webhooks   │      │ • Planning   │      │ • Credentials│
└──────────────┘      └──────────────┘      └──────────────┘
                            │                      │
                            │      ┌───────┐       │
                            └──────│  SYNC │───────┘
                                   │ QUEUE │
                            ┌──────│       │───────┐
                            │      └───────┘       │
                      ┌─────┴─────┐         ┌─────┴─────┐
                      │  SECRET   │         │   FILE    │
                      │  FILTER   │         │   LOCK    │
                      └───────────┘         └───────────┘

                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         MCP INTEGRATIONS                                │
├──────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│   Email      │  LinkedIn    │    Odoo      │  Filesystem  │   Slack     │
│   MCP        │     MCP      │     MCP      │     MCP      │    MCP      │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      OBSERVABILITY & LOGGING                            │
├─────────────────────────────────────────────────────────────────────────┤
│  • Health Monitor  • Audit Logs  • Dashboard  • Alerts                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Security Zones (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SECURITY ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│   PUBLIC INTERNET    │
└──────────┬───────────┘
           │ HTTPS
           ▼
┌──────────────────────┐
│     CLOUD ZONE       │  ◄── Safe Operations Only
│  ┌────────────────┐  │      • Drafting
│  │  Cloud Vault   │  │      • Analysis
│  │                │  │      • Triage
│  │  • Drafts      │  │      • Planning
│  │  • Triage      │  │
│  │  • Plans       │  │  ❌ NO CREDENTIALS
│  └────────────────┘  │  ❌ NO SECRETS
└──────────┬───────────┘
           │
           │    ┌─────────────────┐
           └───►│  SECURITY BOUNDARY│
                │  ┌─────────────┐ │
                │  │Secret Filter│ │
                │  │Markdown Only│ │
                │  │Size Limits  │ │
                │  └─────────────┘ │
                └────────┬─────────┘
                         │
                         ▼
┌──────────────────────┐
│     LOCAL ZONE       │  ◄── Secure Operations
│  ┌────────────────┐  │      • Approvals
│  │  Local Vault   │  │      • Execution
│  │                │  │      • Banking
│  │  • Approvals   │  │      • Credentials
│  │  • Done        │  │
│  │  • Audit       │  │  ✓ CREDENTIALS
│  └────────────────┘  │  ✓ SECRETS
│  ┌────────────────┐  │     (.env file)
│  │ Credentials    │  │
│  │    (.env)      │  │
│  └────────────────┘  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     AUDIT TRAIL      │
│  • JSON Logs         │
│  • Full Traceability │
└──────────────────────┘
```

### Data Flow (ASCII)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       TASK LIFECYCLE FLOW                               │
└──────────────────────────────────────────────────────────────────────────┘

  ┌─────────┐     ┌──────────┐     ┌─────────────┐     ┌───────────┐
  │ EXTERNAL│ ──► │  INBOX   │ ──► │ NEEDS_ACTION│ ──► │ CLOUD     │
  │  EVENT  │     │          │     │             │     │  ZONE     │
  └─────────┘     └──────────┘     └─────────────┘     └───────────┘
                                                          │
                                    ┌─────────────────────┤
                                    │                     ▼
                                    │              ┌─────────────┐
                                    │              │   DRAFTING  │
                                    │              │             │
                                    │              │  • Triage   │
                                    │              │  • Draft    │
                                    │              │  • Analyze  │
                                    │              └─────────────┘
                                    │                     │
                                    │              ┌─────────────┐
                                    └─────────────►│   SYNC      │
                                                   │  Queue      │
                                                   └─────────────┘
                                                         │
                                                         ▼
                                                   ┌─────────────┐
                                                   │   SECRET    │
                                                   │   FILTER    │
                                                   └─────────────┘
                                                         │
                                                ┌────────┴────────┐
                                                │                 │
                                          BLOCKED│                 │PASSED
                                                │                 ▼
                                                │          ┌─────────────┐
                                                │          │  LOCAL      │
                                                │          │  ZONE       │
                                                │          │             │
                                                │          │  • Review   │
                                                │          │  • Approve  │
                                                │          └─────────────┘
                                                │                 │
                                                │          ┌─────────────┐
                                                │          │  APPROVAL   │
                                                │          │  REQUIRED?  │
                                                │          └─────────────┘
                                                │           │         │
                                                │      YES │         │ NO
                                                │           ▼         ▼
                                                │    ┌──────────┐ ┌──────────┐
                                                │    │  HUMAN   │ │ EXECUTE  │
                                                │    │  REVIEW  │ │  ACTION  │
                                                │    └──────────┘ └──────────┘
                                                │         │            │
                                                │    ┌────┴────┐       │
                                                │    │         │       │
                                                │ APPROVE   REJECT    │
                                                │    │         │       │
                                                │    ▼         ▼       │
                                                │ ┌──────┐ ┌──────┐    │
                                                │ │EXEC  │ │DONE  │    │
                                                └─┤      │ │      │◄───┘
                                                  └───┬──┘ └───┬──┘
                                                      │       │
                                                      ▼       ▼
                                                ┌──────────────────┐
                                                │   MCP SERVERS    │
                                                │  • Email         │
                                                │  • LinkedIn      │
                                                │  • Odoo          │
                                                └────────┬─────────┘
                                                         │
                                                         ▼
                                                ┌──────────────────┐
                                                │   AUDIT LOG      │
                                                └────────┬─────────┘
                                                         │
                                                         ▼
                                                ┌──────────────────┐
                                                │     DONE         │
                                                └──────────────────┘
```

---

## Summary

These diagrams illustrate the complete Platinum tier architecture:

1. **System Overview**: All components and their relationships
2. **Zone Architecture**: Cloud/Local specialization and security boundaries
3. **Data Flows**: Complete task lifecycle from detection to completion
4. **Security**: Approval thresholds, secret filtering, credential segregation
5. **MCP Integration**: 6 MCP servers for external actions
6. **Deployment**: Production and simulation deployment options
7. **State Machine**: Task state transitions
8. **Component Interactions**: Delegation, locking, health monitoring

**Key Architectural Principles**:
- ✅ Cloud zone for safe operations (24/7)
- ✅ Local zone for secure operations (credentials)
- ✅ Markdown-only sync with secret filtering
- ✅ Claim-by-move delegation
- ✅ Single-writer dashboard (file locking)
- ✅ Human-in-the-loop for sensitive actions
- ✅ Comprehensive audit trail
- ✅ Health monitoring and auto-recovery

---

**End of Architecture Diagrams**
