# 🏭 Digital FTE — Platinum Tier

**Hackathon 0 Submission**

**For:** Personal AI Employee Hackathon 0
**Built with:** Claude Code

---

## 🏆 Tier Declaration

This project qualifies for **PLATINUM TIER**.

Includes complete implementation of:

- ✅ **Bronze** — Reactive Local Agent
- ✅ **Silver** — Multi-Domain Assistant + MCP + HITL
- ✅ **Gold** — Autonomous Business Employee + Odoo + CEO Briefing
- ✅ **Platinum** — Cloud/Local Split + Delegation Architecture + Production Security

All constitutional requirements satisfied.

---

## 📌 What This Project Is

A **Digital Full-Time Equivalent (FTE)** — an AI employee that:

- Continuously monitors events (Watchers)
- Generates structured plans (Spec-driven reasoning)
- Executes actions via MCP
- Requires human approval for sensitive tasks
- Operates 24/7 using Cloud + Local zones
- Logs every action for auditability

**Architecture inspired by:**
*The Agent Factory Architecture: Building Digital FTEs v1*

---

## 🧠 System Architecture (At a Glance)

### 1️⃣ Perception Layer

- File Watcher
- Gmail Watcher
- Scheduled Tasks
- Business Event Triggers

*Creates structured Markdown tasks.*

### 2️⃣ Reasoning Layer

**Claude:**

- Reads `/Needs_Action`
- Generates `Plan.md`
- Manages state transitions
- Applies guardrails

**State Flow:**
```
Inbox → Needs_Action → Pending_Approval → Approved → Done
```

### 3️⃣ Action Layer (MCP)

**Integrated:**

- Email actions
- LinkedIn drafting
- Odoo accounting (JSON-RPC)
- File operations

*Sensitive actions require approval.*

### 4️⃣ Platinum Hybrid Deployment

**☁️ Cloud:**

- 24/7 monitoring
- Drafting
- Non-sensitive processing

**💻 Local:**

- Approvals
- Financial execution
- Credential-protected MCP calls

**Implements:**

- Claim-by-move rule
- Single-writer dashboard
- Secret segregation

---

## ✔ Tier Verification Summary

### 🥉 Bronze

- Working watcher
- Claude processing
- File transitions
- Agent Skills implemented

### 🥈 Silver

- Multi-domain inputs
- Plan-based execution
- MCP integration
- HITL approvals
- Scheduled automation

### 🥇 Gold

- Odoo integration
- CEO weekly briefing
- Cross-domain reasoning
- Audit logs + retry logic

### 💎 Platinum

- Always-on cloud VM
- Work-zone specialization
- Secure vault sync
- Delegation architecture
- Offline/online recovery demo

---

## 🔐 Security

- No secrets in vault
- `.env`-based credentials
- Human approval gates
- JSON audit logs
- Sensitive actions local-only

---

## ▶ Demo Flow

1. Event detected (Cloud)
2. Task created
3. Plan generated
4. Sensitive step → Approval
5. Local approves
6. MCP executes
7. Logged + archived

---

## ⚙ Quickstart

```bash
git clone https://github.com/Ambreeen17/h0
cd h0
cp .env.example .env
bash setup.sh
claude
```

---

## 📂 Core Structure

```
/watchers
/skills
/mcp
/cloud
/local
/logs
AI_Employee_Vault/
```

---

## 🚀 Why This Matters

This project demonstrates a production-capable Digital FTE with:

- **Structured reasoning**
- **Guardrailed autonomy**
- **Enterprise-style architecture**
- **Secure human oversight**

It goes beyond assistant behavior and implements a true autonomous employee system.

---

**Repository:** https://github.com/Ambreeen17/h0

Built with Claude Code
