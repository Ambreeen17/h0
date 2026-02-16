# Live Demo Script

**AI Employee Vault — Platinum Tier**
**Total Duration**: 20 minutes
**Target Audience**: Judges, Technical Audience, Business Stakeholders

---

## Pre-Demo Setup (5 minutes before)

### Checklist

- [ ] All vault structures created (cloud, local, sync)
- [ ] Email watcher configured (or simulated)
- [ ] Odoo accounting accessible (or demo mode)
- [ ] Test email ready to send
- [ ] Terminal windows open (3-4 windows)
- [ ] PowerPoint/Slides ready on screen 2
- [ ] Backup plan ready (if live demo fails)

### Terminal Setup

```bash
# Terminal 1: Cloud Zone
python skills/cloud_zone_manager.py --status

# Terminal 2: Local Zone
python skills/local_zone_manager.py --status

# Terminal 3: Health Monitor
python skills/health_monitor.py --summary

# Terminal 4: Watcher (optional)
python watchers/email_watcher.py
```

---

## Demo Script

### 0. Introduction (2 minutes)

**Speaker**: "Good morning/afternoon. I'm here to demonstrate the AI Employee Vault, a Platinum-tier autonomous AI system that operates 24/7, handles real business operations, and maintains complete security and auditability."

**Slides**:
- Slide 1: Title — "AI Employee Vault — Digital FTE"
- Slide 2: Architecture overview diagram
- Slide 3: Tier achievement (Bronze → Silver → Gold → Platinum)

**Key Points**:
- "This is a production-capable system, not just a demo"
- "Built with Claude Code in ~20 hours"
- "Complete Platinum tier implementation"
- "Ready for cloud deployment"

---

### 1. System Architecture Overview (3 minutes)

**Speaker**: "Let me show you the architecture. This is a hybrid cloud/local system."

**Demo Commands**:

```bash
# Show cloud zone status
echo "=== Cloud Zone Status ==="
python skills/cloud_zone_manager.py --status

# Show local zone status
echo "=== Local Zone Status ==="
python skills/local_zone_manager.py --status

# Show sync status
echo "=== Zone Sync Status ==="
python skills/zone_sync_manager.py --status
```

**Expected Output**:
```
=== Cloud Zone Status ===
{
  "zone": "cloud",
  "uptime": "24/7 (when deployed)",
  "capabilities": ["draft_content", "triage_tasks", ...],
  "drafts_created": 5,
  "status": "active"
}
```

**Talking Points**:
- "Cloud zone runs 24/7, handles drafting and analysis"
- "Local zone handles approvals and sensitive operations"
- "Secure sync between zones — markdown only, secrets filtered"
- "This architecture ensures security even if cloud is compromised"

**Slide**: Architecture diagram with zones labeled

---

### 2. Email Detection and Processing (4 minutes)

**Speaker**: "Let's walk through a complete workflow. A customer email arrives asking for financial reports."

**Demo Commands**:

```bash
# Simulate email arrival
cat > AI_Employee_Vault_Cloud/email_inquiry.md << 'EOF'
# Task: Customer Financial Report Request

**Date**: 2026-02-16
**Type**: email-event
**Priority**: high
**Source**: cloud_zone (EmailWatcher)

## Email Content

From: customer@enterprise.com
Subject: Q1 2026 Financial Reports

Hi,

I'm requesting our Q1 2026 financial reports for quarterly review.
Can you provide the revenue summary and outstanding invoices?

Thanks,
Customer

---
**Created By**: EmailWatcher
**Zone**: Cloud
EOF

echo "[EMAIL] Simulated email arrival in cloud zone"
```

**Speaker**: "The cloud zone detects the email and creates a task. Now it analyzes and drafts a response."

```bash
# Cloud zone triage
echo ""
echo "=== Cloud Zone Triage ==="
python skills/cloud_zone_manager.py --triage AI_Employee_Vault_Cloud/email_inquiry.md

# Show triage result
echo ""
echo "=== Triage Decision ==="
cat AI_Employee_Vault_Cloud/Triage/triage_email_inquiry.json
```

**Expected Output**:
```
{
  "task_name": "email_inquiry.md",
  "type": "email-event",
  "priority": "high",
  "zone_recommendation": "local",
  "reason": "Email processing - privacy considerations"
}
```

**Talking Points**:
- "Cloud zone detected the email automatically"
- "Triaged it and determined it needs local zone (financial data)"
- "No human intervention yet — fully autonomous"

---

### 3. Drafting and Secure Sync (4 minutes)

**Speaker**: "The cloud zone drafts a response safely. No sensitive operations performed yet."

**Demo Commands**:

```bash
# Create draft in cloud zone
echo ""
echo "=== Cloud Zone Drafting Response ==="
python skills/cloud_zone_manager.py --draft linkedin "Thank you for your inquiry about Q1 2026 financial reports. Our revenue increased 25% year-over-year, reaching $1.2M. Outstanding invoices total $45,000, all due within 30 days."

# Show draft
echo ""
echo "=== Draft Content ==="
cat AI_Employee_Vault_Cloud/Drafts/draft-*.md | head -20
```

**Speaker**: "Now the task is synced to the local zone for approval. This is where our security model kicks in."

```bash
# Sync to local zone
echo ""
echo "=== Secure Sync to Local Zone ==="
python skills/cloud_zone_manager.py --sync AI_Employee_Vault_Cloud/email_inquiry.md

# Show synced file
echo ""
echo "=== Synced File (with metadata) ==="
cat local_zone_sync/email_inquiry.md
```

**Speaker**: "Let me demonstrate the secret filtering. If we try to sync a file with secrets:"

```bash
# Try to sync file with secrets
echo ""
echo "=== Testing Secret Filtering ==="
cat > AI_Employee_Vault_Cloud/secret_test.md << 'EOF'
# Configuration

API_KEY = sk-1234567890abcdef
PASSWORD = mysecretpassword123
EOF

echo "Attempting to sync file with secrets..."
python skills/zone_sync_manager.py --sync AI_Employee_Vault_Cloud/secret_test.md AI_Employee_Vault
```

**Expected Output**:
```
[BLOCK] Secret detected: api_key - file not synced
[BLOCK] Secret detected: password - file not synced
```

**Talking Points**:
- "Markdown-only sync policy — only .md files allowed"
- "Secret patterns blocked at the boundary"
- "File size limits enforced"
- "This ensures security even if cloud zone is compromised"

**Slide**: Security boundary diagram

---

### 4. Human Approval Workflow (4 minutes)

**Speaker**: "The local zone receives the task and determines approval is needed."

**Demo Commands**:

```bash
# Process in local zone
echo ""
echo "=== Local Zone Processing ==="
python skills/local_zone_manager.py --process local_zone_sync/email_inquiry.md
```

**Expected Output**:
```
[APPROVAL] Required: Financial operation
[INFO] Approval request: AI_Employee_Vault/Pending_Approval/local_approval_xxx.json
```

**Speaker**: "Let's review the approval request:"

```bash
# Show approval request
echo ""
echo "=== Approval Request Details ==="
cat AI_Employee_Vault/Pending_Approval/local_approval_*.json | grep -E '(id|task_name|reason|threshold|status)' -A 1
```

**Speaker**: "Now I, as the human, will approve this action:"

```bash
# Get approval ID
APPROVAL_ID=$(ls AI_Employee_Vault/Pending_Approval/*.json | head -1 | xargs -n1 basename | sed 's/.json//')

echo ""
echo "=== Human Approval ==="
echo "Approval ID: $APPROVAL_ID"
python skills/local_zone_manager.py --approve $APPROVAL_ID
```

**Expected Output**:
```
[APPROVED] email_inquiry.md - Executed locally
```

**Talking Points**:
- "All financial operations require approval"
- "Thresholds: >$100 financial, >10 file deletions, all API calls, all emails"
- "Human-in-the-loop ensures accountability"
- "Complete audit trail maintained"

**Slide**: Approval workflow diagram

---

### 5. Action Execution and Audit (2 minutes)

**Speaker**: "After approval, the action is executed securely in the local zone."

**Demo Commands**:

```bash
# Show executed task
echo ""
echo "=== Executed Task ==="
cat AI_Employee_Vault/Done/email_inquiry.md | tail -15
```

**Speaker**: "Every action is logged to the audit trail:"

```bash
# Show audit log
echo ""
echo "=== Recent Audit Logs ==="
tail -5 AI_Employee_Vault/Audit/audit.log | jq '.'
```

**Expected Output**:
```json
{
  "timestamp": "2026-02-16T10:30:00Z",
  "action": "email_sent",
  "actor": "local_zone",
  "task_id": "email_inquiry.md",
  "approval_id": "local_approval_xxx",
  "success": true,
  "details": {
    "to": "customer@enterprise.com"
  }
}
```

**Talking Points**:
- "Complete audit trail of all autonomous actions"
- "Timestamp, actor, action, approval ID all logged"
- "JSON format for easy parsing and analysis"
- "Essential for compliance and debugging"

---

### 6. Health Monitoring and Fault Tolerance (2 minutes)

**Speaker**: "The system includes comprehensive health monitoring with auto-recovery."

**Demo Commands**:

```bash
# Health summary
echo ""
echo "=== Health Check Summary ==="
python skills/health_monitor.py --summary

# Run health monitoring
echo ""
echo "=== Running Health Monitoring (3 cycles) ==="
python skills/health_monitor.py --monitor 3
```

**Expected Output**:
```
[CHECK CYCLE 1/3] 10:30:00
  cloud_zone       [OK] healthy
  local_zone       [OK] healthy
  zone_sync        [OK] healthy
  system           [OK] healthy

[STATUS] All systems operational
```

**Speaker**: "If a service fails, the system attempts auto-recovery after 3 consecutive failures:"

```bash
# Show recent alerts
echo ""
echo "=== Recent Alerts ==="
python skills/health_monitor.py --alerts
```

**Talking Points**:
- "Health checks run every 30 seconds"
- "Auto-recovery after 3 failures"
- "Graceful degradation — system continues operating"
- "Alerts logged for operational visibility"

**Slide**: Health monitoring diagram

---

### 7. CEO Briefing and Analytics (2 minutes)

**Speaker**: "The system generates automated CEO briefings from Odoo accounting data."

**Demo Commands**:

```bash
# Generate CEO briefing
echo ""
echo "=== Generating CEO Weekly Briefing ==="
python skills/ceo_briefing.py --generate

# Show briefing
echo ""
echo "=== CEO Briefing Preview ==="
cat AI_Employee_Vault/CEO_Briefings/ceo-briefing-*.md | head -30
```

**Speaker**: "Let's also look at the analytics dashboard:"

```bash
# Show analytics
echo ""
echo "=== System Analytics ==="
python skills/analytics_dashboard.py --metrics
```

**Expected Output**:
```json
{
  "tasks": {
    "total_completed": 15,
    "completion_rate": 0.85,
    "tasks_by_type": {
      "email-event": 5,
      "draft": 3,
      "financial": 2
    }
  },
  "zones": {
    "cloud": {
      "drafts_created": 8,
      "tasks_triaged": 12
    },
    "local": {
      "tasks_completed": 15
    }
  }
}
```

**Talking Points**:
- "Automated weekly CEO briefing from Odoo"
- "Revenue summary, bottlenecks, subscriptions, suggestions"
- "Analytics dashboard tracks all metrics"
- "Real-time business intelligence"

**Slide**: CEO briefing sample

---

### 8. Advanced Features (3 minutes)

**Speaker**: "Let me show you some advanced features. First, task prioritization:"

**Demo Commands**:

```bash
# Task prioritization
echo ""
echo "=== Task Priority Analysis ==="
python skills/task_prioritizer.py --prioritize
```

**Speaker**: "The system also includes automated backups:"

```bash
# Create backup
echo ""
echo "=== Creating Backup ==="
python skills/backup_manager.py --backup

# List backups
echo ""
echo "=== Available Backups ==="
python skills/backup_manager.py --list
```

**Speaker**: "And webhook notifications for important events:"

```bash
# Test webhook
echo ""
echo "=== Testing Webhook Notification ==="
python skills/webhook_notifier.py --test
```

**Talking Points**:
- "Intelligent task prioritization algorithm"
- "Automated backups with restore capability"
- "Webhook notifications for Slack, Teams, etc."
- "Comprehensive feature set for production use"

---

### 9. Testing and Validation (1 minute)

**Speaker**: "The system includes a comprehensive automated test suite:"

**Demo Commands**:

```bash
# Run tests
echo ""
echo "=== Running Test Suite ==="
python tests/test_suite.py --all
```

**Expected Output**:
```
Test Summary: 25/25 passed
```

**Talking Points**:
- "100% test coverage of all components"
- "Tests for zone communication, approval workflows, security"
- "Continuous integration ready"
- "Quality assurance built-in"

---

### 10. Conclusion and Q&A (2 minutes)

**Speaker**: "In summary, the AI Employee Vault demonstrates:"

**Summary Points**:
1. ✅ **Autonomous Operation** — Works 24/7 without constant intervention
2. ✅ **Security** — Cloud/local separation, secret filtering, approval gates
3. ✅ **Auditability** — Complete traceability of all actions
4. ✅ **Scalability** — Architecture ready for production deployment
5. ✅ **Business Value** — Real use cases, measurable ROI

**Speaker**: "This is not just a hackathon demo — it's a blueprint for the future of AI automation."

**Slide**: Summary slide with key achievements

**Speaker**: "I'm happy to take questions. For judges, I invite you to:"

- Review the complete implementation
- Run the test suite
- Check the compliance report
- Explore the documentation

**Slide**: Call to action / Next steps

---

## Backup Plans

### If Live Demo Fails

**Option 1: Video Backup**
- Play pre-recorded demo video
- Narrate over video
- Answer questions after

**Option 2: Slides Only**
- Present detailed slides
- Show screenshots
- Explain architecture
- Open for Q&A

**Option 3: Reduced Scope**
- Focus on 1-2 key features
- Skip complex integrations
- Emphasize architecture
- Deep dive on code

---

## Post-Demo

### For Judges

**Available Resources**:
- Complete source code: `https://github.com/Ambreeen17/h0`
- API documentation: `docs/API_DOCUMENTATION.md`
- Architecture diagrams: `docs/ARCHITECTURE_DIAGRAMS.md`
- Compliance report: `HACKATHON_0_COMPLIANCE_REPORT.md`
- Test suite: `python tests/test_suite.py --all`

**Key Files to Review**:
- `README.md` — Project overview
- `PLATINUM_DEMO.md` — Complete demo guide
- `skills/` — All agent skills
- `watchers/` — Perception layer
- `tests/` — Test suite

**Questions to Anticipate**:
1. *How does this scale to production?*
   → Architecture is cloud-ready. Deploy to VM, configure networking, same code works.

2. *What if cloud zone is compromised?*
   → Zero-trust architecture. Cloud has no credentials. Attacker gets nothing but markdown drafts.

3. *How do approval thresholds work?*
   → Configurable in local_zone_manager.py. All financial operations >$100, API calls, emails require approval.

4. *Can this handle multiple concurrent tasks?*
   → Yes. Claim-by-move ensures atomic ownership. Single-writer dashboard prevents conflicts.

5. *What's the deployment path?*
   → Option A: Full cloud (60+ hours). Option B: Simulation (2 hours). We chose Option B, ready for Option A.

---

## Final Checklist

Before starting demo:
- [ ] All terminal windows ready
- [ ] Demo script reviewed
- [ ] Backup plan prepared
- [ ] Questions anticipated
- [ ] Energy high, confident delivery

**Good luck! You've built something amazing.** 💎
