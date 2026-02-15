# Platinum Tier Deployment Guide

**Date**: 2026-02-15
**Tier**: 💎 Platinum (Production Hybrid AI Employee)
**Deployment Options**: Full Cloud Deployment (Option A) or Simulation Mode (Option B)
**Status**: ✅ Architecture complete, ready for deployment

---

## Overview

This guide provides deployment instructions for the Platinum tier hybrid AI Employee. The system consists of two zones:

**Cloud Zone** (24/7 Operation):
- Drafting and content creation
- Task triage and classification
- Data analysis and planning
- Pre-processing for local zone

**Local Zone** (Secure On-Premise):
- Approval workflow (human-in-the-loop)
- Sensitive operations execution
- Banking and financial operations
- Credential management

**Zone Sync** (Secure Communication):
- Markdown-only sync policy
- Secret filtering and blocking
- Claim-by-move delegation
- Single-writer dashboard

---

## Deployment Options

### Option A: Full Cloud Deployment (60+ hours)

Deploy cloud zone to actual cloud VM (Oracle/AWS/GCP) for 24/7 operation.

**Prerequisites**:
- Cloud VM account (Oracle Free Tier, AWS EC2, GCP Compute Engine)
- Domain name (optional, for HTTPS)
- Basic networking knowledge

**Estimated Time**: 60+ hours
- Initial setup: 20 hours
- Configuration: 20 hours
- Testing: 10 hours
- Production hardening: 10 hours

### Option B: Simulation Mode (2 hours) ✅ CURRENT

Run zones in separate local folders, simulate network latency, demo all capabilities.

**Prerequisites**:
- Local machine (already set up)
- Python 3.8+
- Existing Platinum tier architecture

**Estimated Time**: 2 hours
- Setup simulation: 30 minutes
- Test all flows: 60 minutes
- Demo preparation: 30 minutes

---

## Option A: Full Cloud Deployment

### Step 1: Provision Cloud VM (Oracle Cloud Free Tier Example)

#### 1.1 Create Oracle Cloud Free Tier Account

1. Go to https://www.oracle.com/cloud/free/
2. Sign up for free tier account
3. Verify email and credit card (required for verification, not charged)

#### 1.2 Create VM Instance

```bash
# In Oracle Cloud Console
# Navigate to: Compute → Instances → Create Instance

Instance Details:
- Name: ai-employee-cloud-zone
- Shape: VM.Standard.E2.1.Micro (Free Tier)
  - 1 OCPU
  - 1 GB RAM
  - 10 GB boot volume
- Image: Oracle Linux 8
- SSH Key: Upload your public SSH key

Networking:
- VCN: Create new VCN
- Subnet: Public subnet
- Public IP: Assign automatically

# Click "Create"
```

**Expected Time**: 15 minutes

#### 1.3 Connect to VM

```bash
# From your local machine
ssh -i ~/.ssh/your_key opc@<YOUR_VM_PUBLIC_IP>

# Example:
# ssh -i ~/.ssh/id_rsa opc@129.146.25.123
```

#### 1.4 Configure VM

```bash
# Update system
sudo dnf update -y

# Install Python 3.8+
sudo dnf install python38 python38-pip python38-devel -y

# Install git
sudo dnf install git -y

# Create working directory
mkdir -p /home/opc/ai-employee
cd /home/opc/ai-employee

# Clone repository
git clone https://github.com/Ambreeen17/h0.git .
```

#### 1.5 Install Dependencies

```bash
# Create virtual environment
python3.8 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install additional cloud dependencies
pip install gunicorn supervisor
```

**Expected Time**: 20 minutes

---

### Step 2: Configure Cloud Zone

#### 2.1 Set Environment Variables

```bash
# Create .env file for cloud zone
cat > /home/opc/ai-employee/.env.cloud << 'EOF_EOF'
# Cloud Zone Configuration
CLOUD_VAULT=/home/opc/ai-employee/AI_Employee_Vault_Cloud
LOCAL_VAULT=/home/opc/ai-employee/AI_Employee_Vault
CLOUD_ZONE_SYNC=/home/opc/ai-employee/cloud_zone_sync
LOCAL_ZONE_SYNC=/home/opc/ai-employee/local_zone_sync

# Zone Configuration
ZONE=cloud

# Email Configuration (for EmailWatcher in cloud)
EMAIL_USER=your-email@example.com
EMAIL_PASS=your-app-password
EMAIL_SERVER=imap.gmail.com
EMAIL_PORT=993

# No credentials in cloud zone!
# Banking, API keys, secrets stay in local zone
EOF_EOF

# Source environment
echo "source /home/opc/ai-employee/.env.cloud" >> ~/.bashrc
source ~/.bashrc
```

#### 2.2 Create Cloud Zone Structure

```bash
# Create vault directories
mkdir -p AI_Employee_Vault_Cloud/{Inbox,Drafts,Triage,Plans}
mkdir -p AI_Employee_Vault/{Inbox,Needs_Action,Done,Pending_Approval,Approved,Rejected,Plans,Content,CEO_Briefings}
mkdir -p zone_sync_queue

# Set permissions
chmod 755 AI_Employee_Vault_Cloud
chmod 700 AI_Employee_Vault  # Local zone more restrictive
```

#### 2.3 Test Cloud Zone Skills

```bash
# Test cloud zone manager
python skills/cloud_zone_manager.py --status

# Expected output:
# {
#   "zone": "cloud",
#   "uptime": "24/7 (when deployed)",
#   "capabilities": [...],
#   "status": "active"
# }
```

**Expected Time**: 15 minutes

---

### Step 3: Configure Watchers for 24/7 Operation

#### 3.1 Create Systemd Service for EmailWatcher

```bash
# Create systemd service file
sudo cat > /etc/systemd/system/ai-employee-email.service << 'EOF_EOF'
[Unit]
Description=AI Employee Email Watcher (Cloud Zone)
After=network.target

[Service]
Type=simple
User=opc
WorkingDirectory=/home/opc/ai-employee
Environment="ZONE=cloud"
EnvironmentFile=/home/opc/ai-employee/.env.cloud
ExecStart=/home/opc/ai-employee/venv/bin/python watchers/email_watcher.py --watch
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF_EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ai-employee-email
sudo systemctl start ai-employee-email

# Check status
sudo systemctl status ai-employee-email
```

#### 3.2 Create Systemd Service for Health Monitor

```bash
# Create systemd service file
sudo cat > /etc/systemd/system/ai-employee-health.service << 'EOF_EOF'
[Unit]
Description=AI Employee Health Monitor (Cloud Zone)
After=network.target

[Service]
Type=simple
User=opc
WorkingDirectory=/home/opc/ai-employee
Environment="ZONE=cloud"
EnvironmentFile=/home/opc/ai-employee/.env.cloud
ExecStart=/home/opc/ai-employee/venv/bin/python skills/health_monitor.py --monitor 1000
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF_EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ai-employee-health
sudo systemctl start ai-employee-health

# Check status
sudo systemctl status ai-employee-health
```

**Expected Time**: 20 minutes

---

### Step 4: Configure Zone Sync (Cloud to Local)

#### 4.1 Set Up Secure File Transfer

**Option 1: SSH File Sync (rsync over SSH)**

```bash
# On cloud VM, generate SSH key pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/ai_employee_sync -N ""

# Add public key to local machine's authorized_keys
# Copy ~/.ssh/ai_employee_sync.pub content to local machine's ~/.ssh/authorized_keys

# Test SSH connection
ssh -i ~/.ssh/ai_employee_sync user@local-machine-ip
```

**Option 2: SFTP File Sync**

```bash
# Install vsftpd on cloud VM (if using FTP)
sudo dnf install vsftpd -y
sudo systemctl enable vsftpd
sudo systemctl start vsftpd
```

#### 4.2 Configure Sync Schedule

```bash
# Create cron job for zone sync
crontab -e

# Add this line (sync every 5 minutes)
*/5 * * * * cd /home/opc/ai-employee && /home/opc/ai-employee/venv/bin/python skills/zone_sync_manager.py --scan >> /var/log/ai-employee-sync.log 2>&1
```

**Expected Time**: 30 minutes

---

### Step 5: Configure Local Zone

#### 5.1 Local Zone Setup (On Your Local Machine)

```bash
# On your local machine (not cloud VM)
cd /path/to/h0

# Create .env file for local zone
cat > .env.local << 'EOF_EOF'
# Local Zone Configuration
LOCAL_VAULT=/path/to/h0/AI_Employee_Vault
CLOUD_VAULT=/path/to/h0/AI_Employee_Vault_Cloud
LOCAL_ZONE_SYNC=/path/to/h0/local_zone_sync
CLOUD_ZONE_SYNC=/path/to/h0/cloud_zone_sync

# Zone Configuration
ZONE=local

# Banking Configuration (LOCAL ONLY!)
BANK_API_KEY=your-banking-api-key
BANK_ACCOUNT_ID=your-account-id

# API Keys (LOCAL ONLY!)
OPENAI_API_KEY=your-openai-key
SLACK_API_KEY=your-slack-key

# Credentials (LOCAL ONLY!)
DATABASE_PASSWORD=your-db-password
# ALL SENSITIVE CREDENTIALS STAY IN LOCAL ZONE
EOF_EOF

# Source environment
echo "source .env.local" >> ~/.bashrc
source ~/.bashrc
```

#### 5.2 Test Local Zone Skills

```bash
# Test local zone manager
python skills/local_zone_manager.py --status

# Expected output:
# {
#   "zone": "local",
#   "status": "secure",
#   "capabilities": ["approve_actions", "sensitive_execution", ...]
# }
```

**Expected Time**: 15 minutes

---

### Step 6: Configure Network and Firewall

#### 6.1 Open Required Ports (Cloud VM)

```bash
# On Oracle Cloud Console
# Navigate to: Networking → VCN → Security Lists

Inbound Rules:
- Port 22 (SSH) from your IP
- Port 80 (HTTP) from 0.0.0.0/0 (optional, for dashboard)
- Port 443 (HTTPS) from 0.0.0.0/0 (optional, for secure dashboard)

# Or using iptables on VM:
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT

# Save rules
sudo service iptables save
```

**Expected Time**: 15 minutes

---

### Step 7: Testing and Validation

#### 7.1 Test Cloud Zone Operations

```bash
# On cloud VM
ssh opc@<cloud-vm-ip>

# Create test task in cloud zone
cat > /home/opc/ai-employee/AI_Employee_Vault_Cloud/test_task.md << 'EOF_TEST'
# Test Task from Cloud Zone

**Type**: test
**Priority**: medium

This is a test task created in cloud zone.
EOF_TEST

# Process task
python skills/cloud_zone_manager.py --triage AI_Employee_Vault_Cloud/test_task.md

# Sync to local zone
python skills/zone_sync_manager.py --scan
```

#### 7.2 Test Local Zone Processing

```bash
# On local machine
cd /path/to/h0

# Process synced task
python skills/local_zone_manager.py --process cloud_zone_sync/test_task.md

# Show approval request
ls -l AI_Employee_Vault/Pending_Approval/

# Approve task
APPROVAL_ID=$(ls AI_Employee_Vault/Pending_Approval/*.json | xargs -n1 basename | sed 's/.json//')
python skills/local_zone_manager.py --approve $APPROVAL_ID
```

#### 7.3 Test Health Monitoring

```bash
# On cloud VM
python skills/health_monitor.py --summary

# On local machine
python skills/health_monitor.py --check local_zone
```

**Expected Time**: 30 minutes

---

### Step 8: Production Hardening

#### 8.1 Set Up Monitoring

```bash
# Install monitoring tools (optional)
sudo dnf install htop iotop -y

# Create log rotation
sudo cat > /etc/logrotate.d/ai-employee << 'EOF_EOF'
/var/log/ai-employee*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF_EOF
```

#### 8.2 Set Up Backup

```bash
# Create backup script
cat > /home/opc/ai-employee/backup.sh << 'EOF_EOF'
#!/bin/bash
BACKUP_DIR=/home/opc/backups
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/ai_employee_$DATE.tar.gz AI_Employee_Vault_Cloud zone_sync_queue

# Keep last 7 days
find $BACKUP_DIR -name "ai_employee_*.tar.gz" -mtime +7 -delete
EOF_EOF

chmod +x /home/opc/ai-employee/backup.sh

# Add to cron (daily backup at 2 AM)
crontab -e
# Add: 0 2 * * * /home/opc/ai-employee/backup.sh
```

#### 8.3 Set Up Alerting (Optional)

```bash
# Install email alerting
sudo dnf install mailx -y

# Configure alert script
cat > /home/opc/ai-employee/alert.sh << 'EOF_EOF'
#!/bin/bash
ALERT_LOG=/var/log/ai-employee-alerts.log
EMAIL=your-email@example.com

if grep -q "critical" $ALERT_LOG; then
    mail -s "AI Employee Critical Alert" $EMAIL < $ALERT_LOG
fi
EOF_EOF

chmod +x /home/opc/ai-employee/alert.sh
```

**Expected Time**: 10 hours

---

## Option B: Simulation Mode (Complete)

### Simulation Setup

Since we chose Option B for the hackathon, the architecture is already complete and tested. Here's how to run the simulation:

#### Step 1: Create Simulation Environment

```bash
# Already done! The vault structures exist:
# - AI_Employee_Vault_Cloud/ (cloud zone)
# - AI_Employee_Vault/ (local zone)
# - zone_sync_queue/ (delegation tracking)
```

#### Step 2: Run Simulation Demo

Follow the `PLATINUM_DEMO.md` guide to demonstrate all capabilities:
- Cloud zone operations (drafting, triage)
- Zone sync with secret filtering
- Local zone approval workflow
- Delegation architecture
- Health monitoring

#### Step 3: Upgrade Path to Option A

When ready for full cloud deployment:
1. Provision cloud VM (Step 1 from Option A)
2. Install dependencies and configure (Step 2-3 from Option A)
3. Set up sync between cloud and local (Step 4 from Option A)
4. Test and validate (Step 7 from Option A)
5. Enable production hardening (Step 8 from Option A)

---

## Troubleshooting

### Issue 1: Cloud Zone Can't Connect to Email

```bash
# Check EmailWatcher service
sudo systemctl status ai-employee-email

# View logs
sudo journalctl -u ai-employee-email -f

# Test IMAP connection manually
python watchers/email_watcher.py --test
```

### Issue 2: Zone Sync Not Working

```bash
# Check sync queue
ls -la zone_sync_queue/

# Test sync manually
python skills/zone_sync_manager.py --scan

# Check sync logs
tail -f /var/log/ai-employee-sync.log
```

### Issue 3: Health Monitor Shows Degraded

```bash
# Check specific service
python skills/health_monitor.py --check cloud_zone
python skills/health_monitor.py --check local_zone

# View alerts
python skills/health_monitor.py --alerts

# Attempt recovery
python skills/health_monitor.py --monitor 1
```

### Issue 4: Approval Workflow Not Working

```bash
# Check pending approvals
ls -la AI_Employee_Vault/Pending_Approval/

# Test approval manually
python skills/local_zone_manager.py --status

# Check approval logs
tail -f local_audit.log
```

---

## Security Best Practices

### Cloud Zone Security

1. **No Credentials**: Never store API keys, passwords, or secrets in cloud zone
2. **Minimal Permissions**: Cloud zone only needs read/write access to its own vault
3. **Network Isolation**: Use security groups to restrict access
4. **Regular Updates**: Keep system and dependencies updated
5. **Monitoring**: Enable health monitoring and alerting

### Local Zone Security

1. **Secure Storage**: All credentials stored in .env.local (never in vault)
2. **Encryption**: Use encryption for sensitive data at rest
3. **Access Control**: Restrict access to local zone vault
4. **Approval Enforcement**: Never bypass approval thresholds
5. **Audit Logging**: Maintain complete audit trail

### Zone Sync Security

1. **Markdown-Only**: Only sync .md files between zones
2. **Secret Filtering**: Block files containing secret patterns
3. **File Size Limits**: Enforce 1MB max file size
4. **Secure Transfer**: Use SSH/SFTP for sync over network
5. **Claim Tracking**: Log all task claims and movements

---

## Performance Optimization

### Cloud Zone Optimization

1. **Horizontal Scaling**: Deploy multiple cloud zone instances behind load balancer
2. **Caching**: Cache frequently accessed data
3. **Async Processing**: Use message queues for heavy tasks
4. **Resource Limits**: Set CPU and memory limits

### Local Zone Optimization

1. **Batch Processing**: Process multiple approvals in batch
2. **Priority Queues**: Prioritize critical tasks
3. **Resource Monitoring**: Monitor CPU, memory, disk usage
4. **Cleanup**: Regular cleanup of old logs and completed tasks

---

## Cost Estimates

### Oracle Cloud Free Tier (Recommended)

- **VM**: Always Free (1 OCPU, 1 GB RAM, 10 GB disk)
- **Network**: 10 TB/month free
- **Email**: $0 (using existing email account)
- **Total**: $0/month

### AWS EC2 (Alternative)

- **VM**: t3.micro ($8/month, 2 vCPU, 1 GB RAM)
- **Network**: 100 GB/month free
- **Email**: $0 (using existing email account)
- **Total**: ~$8/month

### GCP Compute Engine (Alternative)

- **VM**: e2-micro ($6/month, 2 vCPU, 1 GB RAM)
- **Network**: 1 GB/month free
- **Email**: $0 (using existing email account)
- **Total**: ~$6/month

---

## Maintenance

### Daily Tasks

- Check health monitor status
- Review alerts log
- Verify zone sync working

### Weekly Tasks

- Review audit logs
- Check disk usage
- Test backup restoration

### Monthly Tasks

- Update dependencies
- Review and rotate credentials
- Performance optimization
- Security audit

---

## Conclusion

The Platinum tier architecture is **complete and ready for cloud deployment**. You can either:

1. **Deploy to cloud now** (Option A): Follow Option A steps, 60+ hours
2. **Demo in simulation mode** (Option B): Follow PLATINUM_DEMO.md, 2 hours ✅ **COMPLETE**

The architecture is production-ready with:
- Work-zone specialization (cloud vs local)
- Secure delegation architecture
- Fault tolerance and auto-recovery
- Complete security segregation

**Deploy when ready!** 💎✨
