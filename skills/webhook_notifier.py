#!/usr/bin/env python3
"""
Webhook Notifier - Enhanced Feature 2

Send webhook notifications for important events:
- Task completions
- Approval requests
- Health alerts
- System status changes

Usage:
    python skills/webhook_notifier.py --send <event_type> <data>
    python skills/webhook_notifier.py --test
"""

import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
WEBHOOK_ENABLED = os.getenv('WEBHOOK_ENABLED', 'false').lower() == 'true'


class WebhookNotifier:
    """Send webhook notifications for important events."""

    def __init__(self):
        self.webhook_url = WEBHOOK_URL
        self.enabled = WEBHOOK_ENABLED

        if not self.webhook_url:
            print("[WARN] WEBHOOK_URL not configured in .env")

    def send_notification(self, event_type, data):
        """
        Send webhook notification.

        Args:
            event_type: Type of event (task_complete, approval_request, health_alert, etc.)
            data: Event data (dict)
        """
        if not self.enabled or not self.webhook_url:
            print("[INFO] Webhook notifications disabled")
            return False

        payload = {
            'event_type': event_type,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'data': data
        }

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                print(f"[OK] Webhook sent: {event_type}")
                return True
            else:
                print(f"[ERROR] Webhook failed: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Webhook error: {e}")
            return False

    def notify_task_complete(self, task_name, result):
        """Notify when a task is completed."""
        return self.send_notification('task_complete', {
            'task_name': task_name,
            'status': result.get('status', 'completed'),
            'zone': result.get('zone', 'unknown')
        })

    def notify_approval_request(self, approval_id, task_name, reason):
        """Notify when approval is requested."""
        return self.send_notification('approval_request', {
            'approval_id': approval_id,
            'task_name': task_name,
            'reason': reason
        })

    def notify_health_alert(self, service, status, message):
        """Notify when health issue detected."""
        return self.send_notification('health_alert', {
            'service': service,
            'status': status,
            'message': message
        })

    def notify_system_status(self, overall_status, details):
        """Notify system status change."""
        return self.send_notification('system_status', {
            'overall_status': overall_status,
            'details': details
        })


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Webhook Notifier')
    parser.add_argument('--send', nargs=2, metavar=('EVENT_TYPE', 'DATA_JSON'),
                       help='Send notification')
    parser.add_argument('--test', action='store_true',
                       help='Send test notification')
    args = parser.parse_args()

    notifier = WebhookNotifier()

    if args.test:
        print("Sending test notification...")
        notifier.send_notification('test', {
            'message': 'Test notification from AI Employee Vault'
        })

    if args.send:
        event_type, data_json = args.send
        try:
            data = json.loads(data_json)
            notifier.send_notification(event_type, data)
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON data: {data_json}")

    if not any([args.send, args.test]):
        parser.print_help()


if __name__ == '__main__':
    main()
