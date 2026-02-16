# AI Employee Vault - API Documentation

**Version**: 1.0.0
**Last Updated**: 2026-02-16
**Tier**: Platinum

---

## Table of Contents

1. [Overview](#overview)
2. [Skills API](#skills-api)
3. [Watchers API](#watchers-api)
4. [MCP Integrations](#mcp-integrations)
5. [Zone Management API](#zone-management-api)
6. [Data Models](#data-models)
7. [Error Handling](#error-handling)
8. [Security Considerations](#security-considerations)

---

## Overview

The AI Employee Vault system provides a comprehensive API for managing autonomous AI operations across cloud and local zones. All components follow the Agent Skills pattern - reusable, testable Python modules with well-defined contracts.

### Architecture Principles

- **Local-First**: All state managed in Obsidian vault (file-based)
- **Zone Separation**: Cloud (drafting/triage) vs Local (approvals/sensitive)
- **Human-in-the-Loop**: Sensitive actions require approval
- **Audit Trail**: All actions logged to JSON
- **Markdown-Only Sync**: Only .md files synced between zones

---

## Skills API

### CloudZoneManager

**Module**: `skills/cloud_zone_manager.py`
**Purpose**: Manages cloud-zone operations (drafting, triage, analysis)

#### Class: `CloudZoneManager`

```python
class CloudZoneManager:
    """Manages cloud-zone operations for Platinum tier."""
```

##### Methods

###### `__init__()`

Initializes the cloud zone manager.

**Returns**: `CloudZoneManager` instance

**Example**:
```python
from skills.cloud_zone_manager import CloudZoneManager
manager = CloudZoneManager()
```

---

###### `can_handle_in_cloud(task_type: str, task_content: str) -> Tuple[bool, str]`

Determines if a task can be handled in the cloud zone.

**Parameters**:
- `task_type` (str): Type of task (draft, analyze, triage, plan, etc.)
- `task_content` (str): Task content to analyze for sensitive keywords

**Returns**: `Tuple[bool, str]`
- `bool`: True if task can be handled in cloud, False otherwise
- `str`: Reason for decision

**Sensitive Keywords**: `approve`, `authorization`, `credential`, `password`, `banking`, `financial transaction`, `api_key`, `secret`, `token`, `private_key`, `sensitive`

**Example**:
```python
can_handle, reason = manager.can_handle_in_cloud('draft', 'Create LinkedIn post')
# Returns: (True, 'Appropriate for cloud zone')

can_handle, reason = manager.can_handle_in_cloud('approve', 'Send money')
# Returns: (False, 'Contains sensitive keywords')
```

---

###### `prepare_for_local_zone(task_path: Path) -> Path`

Prepares a task for local zone processing by creating a sync package.

**Parameters**:
- `task_path` (Path): Path to task file

**Returns**: `Path` - Path to sync package JSON file

**Side Effects**:
- Creates sync package in `CLOUD_ZONE_SYNC` directory
- Marks task as requiring approval

**Example**:
```python
sync_file = manager.prepare_for_local_zone(Path('task.md'))
# Creates: ./cloud_zone_sync/sync_task.md.json
```

---

###### `draft_content_in_cloud(topic: str, content: str) -> Path`

Drafts content in the cloud zone (safe, non-sensitive operation).

**Parameters**:
- `topic` (str): Content type (linkedin, email, general, etc.)
- `content` (str): Draft content

**Returns**: `Path` - Path to created draft file

**Side Effects**:
- Creates draft in `AI_Employee_Vault_Cloud/Drafts/`
- Adds timestamp and zone metadata

**Example**:
```python
draft_path = manager.draft_content_in_cloud(
    'linkedin',
    'Excited to announce our Q1 results!'
)
# Creates: AI_Employee_Vault_Cloud/Drafts/draft-2026-02-16T10-30-00.md
```

---

###### `triage_tasks(task_path: Path) -> Dict`

Triage and categorize tasks for efficient processing.

**Parameters**:
- `task_path` (Path): Path to task file

**Returns**: `Dict` - Triage report with keys:
- `task_name` (str): Name of task
- `type` (str): Task type
- `priority` (str): Priority level
- `zone_recommendation` (str): 'cloud' or 'local'
- `reason` (str): Explanation for recommendation
- `triaged_at` (str): ISO timestamp

**Side Effects**:
- Creates triage report in `AI_Employee_Vault_Cloud/Triage/`

**Example**:
```python
triage = manager.triage_tasks(Path('task.md'))
# Returns: {
#   'task_name': 'task.md',
#   'type': 'email-event',
#   'priority': 'high',
#   'zone_recommendation': 'local',
#   'reason': 'Email processing - privacy considerations',
#   'triaged_at': '2026-02-16T10:30:00Z'
# }
```

---

###### `sync_to_local_zone(task_path: Path) -> Path`

Syncs a task to local zone (markdown-only policy enforced).

**Parameters**:
- `task_path` (Path): Path to task file

**Returns**: `Path` - Path to synced file in local zone, or None if blocked

**Blocking Rules**:
- Only .md files allowed
- File must be ≤ 1MB
- Must not contain secret patterns

**Side Effects**:
- Creates file in `LOCAL_ZONE_SYNC/`
- Adds sync metadata

**Example**:
```python
local_file = manager.sync_to_local_zone(Path('draft.md'))
# Creates: ./local_zone_sync/draft.md
```

---

###### `get_cloud_status() -> Dict`

Gets current cloud zone status and metrics.

**Returns**: `Dict` with keys:
- `zone` (str): 'cloud'
- `uptime` (str): '24/7 (when deployed)'
- `capabilities` (List[str]): List of cloud capabilities
- `drafts_created` (int): Number of drafts in cloud zone
- `tasks_triaged` (int): Number of triaged tasks
- `pending_sync` (int): Number of tasks pending sync
- `status` (str): 'active'

**Example**:
```python
status = manager.get_cloud_status()
# Returns: {
#   'zone': 'cloud',
#   'uptime': '24/7 (when deployed)',
#   'capabilities': ['draft_content', 'triage_tasks', ...],
#   'drafts_created': 5,
#   'tasks_triaged': 10,
#   'pending_sync': 2,
#   'status': 'active'
# }
```

---

#### Command-Line Interface

```bash
# Create draft
python skills/cloud_zone_manager.py --draft linkedin "Post content here"

# Triage task
python skills/cloud_zone_manager.py --triage path/to/task.md

# Sync to local zone
python skills/cloud_zone_manager.py --sync path/to/task.md

# Show status
python skills/cloud_zone_manager.py --status
```

---

### LocalZoneManager

**Module**: `skills/local_zone_manager.py`
**Purpose**: Manages local zone operations (approvals, sensitive execution)

#### Class: `LocalZoneManager`

```python
class LocalZoneManager:
    """Manages local zone security and approvals."""
```

##### Methods

###### `__init__()`

Initializes the local zone manager.

**Returns**: `LocalZoneManager` instance

---

###### `process_task(task_path: Path) -> Dict`

Process a task in local zone (checks if approval required).

**Parameters**:
- `task_path` (Path): Path to task file

**Returns**: `Dict` with keys:
- `task_name` (str): Task name
- `requires_approval` (bool): Whether approval is needed
- `reason` (str): Reason if approval required
- `status` (str): Processing status

**Approval Thresholds**:
- Financial operations > $100
- File deletion > 10 files
- All API calls
- All email sending
- All credential access

**Example**:
```python
result = manager.process_task(Path('task.md'))
# Returns: {
#   'task_name': 'task.md',
#   'requires_approval': True,
#   'reason': 'Financial operation exceeds $100 threshold',
#   'status': 'pending_approval'
# }
```

---

###### `approve_action(approval_id: str) -> bool`

Approve a pending action.

**Parameters**:
- `approval_id` (str): Approval request ID

**Returns**: `bool` - True if approved successfully

**Side Effects**:
- Moves approval from Pending_Approval to Approved
- Executes the action
- Creates audit log entry

**Example**:
```python
success = manager.approve_action('local_approval_2026-02-16T10-30-00')
# Returns: True
```

---

###### `reject_action(approval_id: str, reason: str) -> bool`

Reject a pending action.

**Parameters**:
- `approval_id` (str): Approval request ID
- `reason` (str): Reason for rejection

**Returns**: `bool` - True if rejected successfully

**Side Effects**:
- Moves approval from Pending_Approval to Rejected
- Logs rejection with reason

**Example**:
```python
success = manager.reject_action(
    'local_approval_2026-02-16T10-30-00',
    'Insufficient documentation'
)
```

---

###### `execute_sensitive_action(action_type: str, params: Dict) -> Dict`

Execute a sensitive action (after approval).

**Parameters**:
- `action_type` (str): Type of action (email_send, api_call, banking, etc.)
- `params` (Dict): Action parameters

**Returns**: `Dict` with keys:
- `success` (bool): Execution success status
- `result` (Any): Action result
- `executed_at` (str): ISO timestamp
- `zone` (str): 'local'

**Security**: Only executes after approval. Never syncs credentials.

**Example**:
```python
result = manager.execute_sensitive_action(
    'email_send',
    {'to': 'customer@example.com', 'subject': 'Report', 'body': '...'}
)
# Returns: {
#   'success': True,
#   'result': 'Email sent successfully',
#   'executed_at': '2026-02-16T10:30:00Z',
#   'zone': 'local'
# }
```

---

#### Command-Line Interface

```bash
# Process task
python skills/local_zone_manager.py --process path/to/task.md

# Approve action
python skills/local_zone_manager.py --approve <approval_id>

# Reject action
python skills/local_zone_manager.py --reject <approval_id> <reason>

# Show status
python skills/local_zone_manager.py --status
```

---

### ZoneSyncManager

**Module**: `skills/zone_sync_manager.py`
**Purpose**: Manages secure delegation architecture between zones

#### Class: `ZoneSyncManager`

```python
class ZoneSyncManager:
    """Manages secure synchronization between zones."""
```

##### Methods

###### `claim_task(task_path: Path, from_zone: str, to_zone: str) -> Tuple[Path, Path]`

Claim a task by moving it between zones (Claim-by-Move rule).

**Parameters**:
- `task_path` (Path): Path to task file
- `from_zone` (str): Source zone name
- `to_zone` (str): Destination zone name

**Returns**: `Tuple[Path, Path]`
- Path to claim file
- Path to moved task

**Side Effects**:
- Creates claim file in `zone_sync_queue/`
- Moves task file to destination zone
- Atomic operation (prevents race conditions)

**Example**:
```python
claim_file, task_path = manager.claim_task(
    Path('AI_Employee_Vault_Cloud/task.md'),
    'AI_Employee_Vault_Cloud',
    'AI_Employee_Vault'
)
# Creates: zone_sync_queue/claim_task_2026-02-16T10-30-00.[cloud].json
# Moves: task.md to AI_Employee_Vault/
```

---

###### `sync_file(source_path: Path, dest_zone: str) -> bool`

Sync file between zones (markdown-only policy enforced).

**Parameters**:
- `source_path` (Path): Source file path
- `dest_zone` (str): Destination zone path

**Returns**: `bool` - True if synced successfully, False if blocked

**Sync Rules**:
- Only .md files allowed
- Max file size: 1MB
- Excludes: .env, credential, secret, token patterns
- Blocks secret patterns: password, api_key, secret, token, credential, private_key

**Side Effects**:
- Creates copy in destination zone
- Creates sync receipt in `zone_sync_queue/`

**Example**:
```python
success = manager.sync_file(
    Path('AI_Employee_Vault_Cloud/draft.md'),
    'AI_Employee_Vault'
)
# Returns: True
# Creates: AI_Employee_Vault/draft.md
# Creates: zone_sync_queue/sync_receipt_draft.json
```

---

###### `update_dashboard_single_writer(update_func: Callable) -> bool`

Update dashboard with single-writer guarantee (uses file locking).

**Parameters**:
- `update_func` (Callable): Function that generates dashboard content

**Returns**: `bool` - True if updated successfully

**Concurrency Control**:
- Uses `filelock` library
- Acquires lock before writing
- 10-second timeout
- Prevents concurrent write conflicts

**Example**:
```python
def generate_dashboard():
    return "# Dashboard\n\nUpdated content..."

success = manager.update_dashboard_single_writer(generate_dashboard)
# Returns: True
```

---

###### `scan_and_sync() -> int`

Scan for files to sync and process them.

**Returns**: `int` - Number of files synced

**Side Effects**:
- Scans cloud zone for files not in local zone
- Syncs eligible files
- Creates sync receipts

**Example**:
```python
count = manager.scan_and_sync()
# Returns: 3 (synced 3 files)
```

---

###### `get_delegation_status() -> Dict`

Get current delegation and sync status.

**Returns**: `Dict` with keys:
- `zone_sync_active` (bool): Sync status
- `pending_claims` (int): Number of pending claims
- `completed_syncs` (int): Number of completed syncs
- `sync_rules` (Dict): Active sync rules
- `delegation_architecture` (Dict): Architecture description

**Example**:
```python
status = manager.get_delegation_status()
# Returns: {
#   'zone_sync_active': True,
#   'pending_claims': 2,
#   'completed_syncs': 15,
#   'sync_rules': {...},
#   'delegation_architecture': {...}
# }
```

---

#### Command-Line Interface

```bash
# Claim task
python skills/zone_sync_manager.py --claim path/to/task.md AI_Employee_Vault

# Sync file
python skills/zone_sync_manager.py --sync path/to/file.md AI_Employee_Vault

# Scan and sync
python skills/zone_sync_manager.py --scan

# Show status
python skills/zone_sync_manager.py --status
```

---

### HealthMonitor

**Module**: `skills/health_monitor.py`
**Purpose**: Monitors system health and implements fault tolerance

#### Class: `HealthMonitor`

```python
class HealthMonitor:
    """Monitors system health and implements fault tolerance."""
```

##### Methods

###### `check_service_health(service_name: str) -> str`

Check health of a specific service.

**Parameters**:
- `service_name` (str): Service name ('cloud_zone', 'local_zone', 'zone_sync', 'system')

**Returns**: `str` - 'healthy', 'degraded', or 'critical'

**Health Checks**:
- **cloud_zone**: Vault exists and writable
- **local_zone**: Vault exists and pending approvals < 10
- **zone_sync**: Sync queue exists and pending claims < 20
- **system**: CPU < 90%, memory < 90%, disk < 90%

**Example**:
```python
status = monitor.check_service_health('cloud_zone')
# Returns: 'healthy'
```

---

###### `attempt_recovery(service_name: str) -> bool`

Attempt to recover a failed service.

**Parameters**:
- `service_name` (str): Service name to recover

**Returns**: `bool` - True if recovery successful

**Recovery Actions**:
- **cloud_zone**: Recreate cloud vault directory
- **zone_sync**: Clear stuck syncs and recreate queue

**Example**:
```python
success = monitor.attempt_recovery('cloud_zone')
# Returns: True
```

---

###### `run_health_checks(iterations: int = 10)`

Run continuous health monitoring cycles.

**Parameters**:
- `iterations` (int): Number of check cycles (default: 10)

**Side Effects**:
- Logs health status to `platinum_health.log`
- Logs alerts to `platinum_alerts.log`
- Attempts auto-recovery after 3 consecutive failures
- Prints real-time status to console

**Auto-Recovery**:
- Triggered after 3 consecutive failures
- Logs recovery attempts
- Resets failure counter on success

**Example**:
```python
monitor.run_health_checks(iterations=10)
# Runs 10 cycles, 30 seconds apart
```

---

###### `get_health_summary() -> Dict`

Get summary of system health.

**Returns**: `Dict` with keys for each service and overall status

**Example**:
```python
summary = monitor.get_health_summary()
# Returns: {
#   'cloud_zone': 'healthy',
#   'local_zone': 'healthy',
#   'zone_sync': 'healthy',
#   'system': 'healthy',
#   'overall': 'healthy'
# }
```

---

#### Command-Line Interface

```bash
# Check specific service
python skills/health_monitor.py --check cloud_zone

# Run continuous monitoring
python skills/health_monitor.py --monitor 10

# Show health summary
python skills/health_monitor.py --summary

# Show recent alerts
python skills/health_monitor.py --alerts
```

---

## Watchers API

### EmailWatcher

**Module**: `watchers/email_watcher.py`
**Purpose**: Monitors email inbox and creates tasks for new emails

#### Class: `EmailWatcher`

```python
class EmailWatcher:
    """Monitors Gmail inbox and creates tasks for new emails."""
```

##### Methods

###### `__init__(vault_path: str = 'AI_Employee_Vault')`

Initialize email watcher.

**Parameters**:
- `vault_path` (str): Path to vault inbox folder

---

###### `check_email() -> List[Dict]`

Check for new emails and create tasks.

**Returns**: `List[Dict]` - List of created task metadata

**Environment Variables Required**:
- `GMAIL_API_KEY`: Gmail API credentials
- `WATCHER_LABEL`: Gmail label to monitor (default: 'AI_Process')

**Example**:
```python
watcher = EmailWatcher()
tasks = watcher.check_email()
# Returns: [
#   {'task_id': 'task-2026-02-16T10-30-00', 'email_id': '...'},
#   ...
# ]
```

---

### FileSystemWatcher

**Module**: `watchers/filesystem_watcher.py`
**Purpose**: Monitors directory for new files and creates tasks

#### Class: `FileSystemWatcher`

```python
class FileSystemWatcher:
    """Monitors directory for new files and creates tasks."""
```

##### Methods

###### `__init__(watch_dir: str, vault_path: str = 'AI_Employee_Vault')`

Initialize file system watcher.

**Parameters**:
- `watch_dir` (str): Directory to monitor
- `vault_path` (str): Path to vault inbox folder

---

###### `start_watching()`

Start monitoring directory (blocking call).

**Environment Variables**:
- `WATCH_DIRECTORY`: Directory to watch (default: ~/Downloads)
- `WATCHER_EXTENSIONS`: File extensions to watch (default: .pdf,.doc,.docx,.txt,.md,.jpg,.png)

**Example**:
```python
watcher = FileSystemWatcher('~/Downloads', 'AI_Employee_Vault')
watcher.start_watching()  # Blocks until Ctrl+C
```

---

## MCP Integrations

### MCP Configuration

**File**: `multi_mcp_config.json`
**Purpose**: Configures 6 MCP servers for different capabilities

#### Servers

1. **email-mcp-server**: Email operations (send, read, organize)
2. **linkedin-mcp-server**: LinkedIn content drafting and publishing
3. **odoo-mcp-server**: Odoo accounting integration (JSON-RPC)
4. **filesystem-mcp-server**: File operations (read, write, organize)
5. **slack-mcp-server**: Slack messaging and notifications
6. **calendar-mcp-server**: Calendar event management

#### MCP Actions API

**Module**: `skills/mcp_actions.py`

```python
class MCPActions:
    """Executes actions via MCP servers."""
```

##### Methods

###### `execute_email_action(action: str, params: Dict) -> Dict`

Execute email action via Email MCP.

**Parameters**:
- `action` (str): Action type ('send', 'read', 'organize')
- `params` (Dict): Action parameters

**Returns**: `Dict` - Result from MCP server

**Security**: Requires approval for send action.

---

###### `execute_linkedin_action(action: str, params: Dict) -> Dict`

Execute LinkedIn action via LinkedIn MCP.

**Parameters**:
- `action` (str): Action type ('draft', 'publish', 'schedule')
- `params` (Dict): Action parameters

**Returns**: `Dict` - Result from MCP server

---

###### `execute_odoo_action(action: str, params: Dict) -> Dict`

Execute Odoo accounting action via Odoo MCP.

**Parameters**:
- `action` (str): Action type ('query_invoice', 'create_payment', 'get_report')
- `params` (Dict): Action parameters (requires Odoo credentials)

**Returns**: `Dict` - Financial data from Odoo

**Security**: All Odoo actions require approval.

---

## Data Models

### Task Model

```yaml
# AI_Employee_Vault/Needs_Action/task-YYYY-MM-DDTHH-MM-SS.md

# Task: <Task Title>

**Date**: 2026-02-16
**Type**: <task_type>
**Priority**: <high|medium|low>
**Source**: <source_system>
**Status**: <pending|in_progress|completed|blocked>

## Context

<Task context and background>

## Requirements

<Specific requirements for completion>

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

---

**Created By**: <Watcher|User>
**Zone**: <cloud|local>
**Detected At**: 2026-02-16T10:30:00Z
```

### Approval Request Model

```json
{
  "id": "local_approval_2026-02-16T10-30-00",
  "task_name": "task_name",
  "action_type": "email_send|api_call|banking|file_delete",
  "reason": "Financial operation exceeds $100 threshold",
  "threshold": ">0",
  "params": {
    "to": "customer@example.com",
    "subject": "Report"
  },
  "created_at": "2026-02-16T10:30:00Z",
  "status": "pending"
}
```

### Audit Log Model

```json
{
  "timestamp": "2026-02-16T10:30:00Z",
  "action": "email_sent",
  "actor": "local_zone",
  "task_id": "task-2026-02-16T10-30-00",
  "approval_id": "local_approval_2026-02-16T10-29-00",
  "success": true,
  "details": {
    "to": "customer@example.com",
    "subject": "Financial Report"
  }
}
```

### Triage Model

```json
{
  "task_name": "task.md",
  "type": "email-event",
  "priority": "high",
  "zone_recommendation": "local",
  "reason": "Email processing - privacy considerations",
  "triaged_at": "2026-02-16T10:30:00Z"
}
```

---

## Error Handling

### Error Codes

| Code | Description | Action |
|------|-------------|--------|
| `E001` | Vault not found | Create vault structure |
| `E002` | Invalid task format | Validate task schema |
| `E003` | Approval timeout | Resubmit approval request |
| `E004` | Sync blocked (secret) | Remove secrets from file |
| `E005` | Zone unreachable | Check network connectivity |
| `E006` | File too large | Compress or split file |
| `E007` | Lock timeout | Retry after delay |
| `E008` | MCP connection failed | Check MCP server status |
| `E009` | Credential missing | Set environment variable |
| `E010` | Health check failed | Run recovery procedures |

### Exception Handling Pattern

```python
try:
    result = manager.sync_to_local_zone(task_path)
except FileNotFoundError as e:
    logger.error(f"E001: Vault not found - {e}")
    create_vault_structure()
except PermissionError as e:
    logger.error(f"E003: Permission denied - {e}")
    raise ApprovalRequiredError("Insufficient permissions")
except Exception as e:
    logger.error(f"E999: Unexpected error - {e}")
    raise
```

---

## Security Considerations

### Credential Management

✅ **DO**:
- Store all credentials in `.env` file
- Use environment variables for all secrets
- Rotate credentials regularly
- Use scoped API keys with minimal permissions

❌ **DON'T**:
- Never store credentials in vault
- Never hardcode secrets in code
- Never log sensitive data
- Never sync credentials between zones

### Approval Thresholds

| Action | Threshold | Approval Required |
|--------|-----------|-------------------|
| Email send | All | Yes |
| API call | All | Yes |
| Banking | >$0 | Yes |
| File delete | >10 files | Yes |
| Financial | >$100 | Yes |
| Content draft | None | No |

### Zone Security Boundaries

**Cloud Zone** (Safe Operations):
- Content drafting
- Data analysis
- Triage and classification
- Plan generation
- Pre-processing

**Local Zone** (Secure Operations):
- Approval decisions
- Credential access
- Banking operations
- Sensitive execution
- Final authorization

### Audit Logging

All autonomous actions are logged with:
- Timestamp (UTC)
- Actor (zone/agent)
- Action type
- Task ID
- Approval ID (if applicable)
- Success status
- Details (sanitized)

Logs stored in:
- `platinum_health.log` - Health monitoring
- `platinum_alerts.log` - Alerts and recovery
- `AI_Employee_Vault/Audit/` - Action audit logs

---

## API Versioning

This documentation is for API version 1.0.0.

Versioning follows semantic versioning:
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

---

## Support

For issues or questions:
- Check constitution: `.specify/memory/constitution.md`
- Review demo guide: `PLATINUM_DEMO.md`
- Run health check: `python skills/health_monitor.py --summary`

---

**End of API Documentation**
