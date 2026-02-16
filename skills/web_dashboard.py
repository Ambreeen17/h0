#!/usr/bin/env python3
"""
AI Employee Web Dashboard
Real-time web interface for monitoring the AI Employee system
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, render_template, jsonify, send_from_directory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VAULT_BASE = Path(os.getenv('VAULT_BASE', 'AI_Employee_Vault'))
VAULT_CLOUD = Path(os.getenv('VAULT_CLOUD', 'AI_Employee_Vault_CLOUD'))
ZONE_SYNC_QUEUE = Path('zone_sync_queue')
AUDIT_LOG = Path('audit.log.jsonl')

app = Flask(__name__)

class DashboardData:
    """Gathers dashboard data from the file system."""

    def __init__(self):
        self.vault_base = VAULT_BASE
        self.vault_cloud = VAULT_CLOUD
        self.zone_sync = ZONE_SYNC_QUEUE
        self.audit_log = AUDIT_LOG

    def get_task_counts(self):
        """Get task counts from all queues."""
        counts = {
            'inbox': len(list(self.vault_base.glob('Inbox/*.md'))),
            'needs_action': len(list(self.vault_base.glob('Needs_Action/*.md'))),
            'done': len(list(self.vault_base.glob('Done/*.md'))),
            'pending_approval': len(list(self.vault_base.glob('Pending_Approval/*.json'))),
            'approved': len(list(self.vault_base.glob('Approved/*.md'))),
            'rejected': len(list(self.vault_base.glob('Rejected/*.md'))),
            'cloud_drafts': len(list(self.vault_cloud.glob('Drafts/*.md'))),
            'cloud_tasks': len(list(self.vault_cloud.glob('*.md'))),
        }
        return counts

    def get_recent_tasks(self, folder, limit=10):
        """Get recent tasks from a folder."""
        tasks = []
        for task_file in sorted(self.vault_base.glob(f'{folder}/*.md'), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]:
            try:
                content = task_file.read_text(encoding='utf-8')
                # Extract title
                title = task_file.stem
                for line in content.split('\n')[:5]:
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break

                # Extract timestamp
                timestamp = datetime.fromtimestamp(task_file.stat().st_mtime, tz=timezone.utc).isoformat()

                tasks.append({
                    'title': title,
                    'filename': task_file.name,
                    'timestamp': timestamp,
                    'size': task_file.stat().st_size
                })
            except Exception as e:
                print(f"Error reading {task_file}: {e}")
        return tasks

    def get_zone_status(self):
        """Get status of cloud and local zones."""
        # Cloud zone stats
        cloud_tasks = list(self.vault_cloud.glob('*.md'))
        cloud_drafts = list(self.vault_cloud.glob('Drafts/*.md'))

        # Local zone stats
        local_done = list(self.vault_base.glob('Done/*.md'))
        local_approvals = list(self.vault_base.glob('Pending_Approval/*.json'))

        # Sync queue stats
        sync_files = list(self.zone_sync.glob('*.json'))

        return {
            'cloud': {
                'tasks': len(cloud_tasks),
                'drafts': len(cloud_drafts),
                'status': 'active'
            },
            'local': {
                'completed': len(local_done),
                'pending_approvals': len(local_approvals),
                'status': 'active'
            },
            'sync': {
                'queue_size': len(sync_files),
                'status': 'active'
            }
        }

    def get_recent_activity(self, limit=20):
        """Get recent activity from audit log."""
        activity = []
        try:
            if self.audit_log.exists():
                with open(self.audit_log, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines[-limit:]:
                        try:
                            entry = json.loads(line.strip())
                            activity.append(entry)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"Error reading audit log: {e}")
        return list(reversed(activity))

    def get_metrics(self):
        """Calculate system metrics."""
        counts = self.get_task_counts()

        total_tasks = counts['done'] + counts['approved'] + counts['rejected']
        if total_tasks > 0:
            completion_rate = counts['done'] / (counts['done'] + counts['needs_action'] + counts['inbox'])
        else:
            completion_rate = 0

        return {
            'total_completed': counts['done'],
            'completion_rate': round(completion_rate * 100, 1),
            'tasks_in_queue': counts['needs_action'],
            'pending_approvals': counts['pending_approval'],
            'cloud_drafts': counts['cloud_drafts']
        }

dashboard_data = DashboardData()

@app.route('/')
def index():
    """Render main dashboard."""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """API endpoint for system status."""
    return jsonify({
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'counts': dashboard_data.get_task_counts(),
        'zones': dashboard_data.get_zone_status(),
        'metrics': dashboard_data.get_metrics()
    })

@app.route('/api/tasks/<queue>')
def api_tasks(queue):
    """API endpoint for task queues."""
    valid_queues = ['inbox', 'needs_action', 'done', 'pending_approval']
    if queue not in valid_queues:
        return jsonify({'error': 'Invalid queue'}), 400

    folder_map = {
        'inbox': 'Inbox',
        'needs_action': 'Needs_Action',
        'done': 'Done',
        'pending_approval': 'Pending_Approval'
    }

    # For pending approvals, we return JSON files
    if queue == 'pending_approval':
        tasks = []
        for task_file in sorted(dashboard_data.vault_base.glob(f'{folder_map[queue]}/*.json'),
                               key=lambda p: p.stat().st_mtime, reverse=True)[:20]:
            try:
                with open(task_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data['filename'] = task_file.name
                tasks.append(data)
            except Exception as e:
                print(f"Error reading {task_file}: {e}")
        return jsonify(tasks)

    # For markdown task files
    return jsonify(dashboard_data.get_recent_tasks(folder_map[queue]))

@app.route('/api/activity')
def api_activity():
    """API endpoint for recent activity."""
    return jsonify(dashboard_data.get_recent_activity())

@app.route('/api/zone/<zone>')
def api_zone(zone):
    """API endpoint for zone-specific status."""
    zones = dashboard_data.get_zone_status()
    if zone not in zones:
        return jsonify({'error': 'Invalid zone'}), 400
    return jsonify(zones[zone])

if __name__ == '__main__':
    print("=" * 60)
    print("AI Employee Web Dashboard")
    print("=" * 60)
    print(f"Starting server at http://localhost:5000")
    print(f"Vault: {VAULT_BASE}")
    print(f"Cloud Zone: {VAULT_CLOUD}")
    print("=" * 60)
    print("\nOpen your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")

    app.run(host='0.0.0.0', port=5000, debug=False)
