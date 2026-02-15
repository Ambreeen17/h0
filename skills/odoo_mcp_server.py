#!/usr/bin/env python3
"""
Odoo MCP Server - Gold Tier Accounting Integration

Provides JSON-RPC interface to Odoo Community 19+ for financial data.
This is a simplified implementation for demonstration.

Requirements:
- requests: pip install requests
- python-dotenv: pip install python-dotenv
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
ODOO_DB = os.getenv('ODOO_DB', 'odoo_db')
ODOO_USER = os.getenv('ODOO_USER', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')


class OdooMCPServer:
    """Simplified Odoe MCP server for demonstration."""

    def __init__(self):
        self.base_url = ODOO_URL
        self.db = ODOO_DB
        self.user = ODOO_USER
        self.password = ODOO_PASSWORD

    def _call_odoo(self, model, method, domain=None, fields=None):
        """
        Call Odoo via JSON-RPC (simplified implementation).

        In production, this would use xmlrpc.client.ServerProxy
        For demo purposes, returns mock data.
        """
        # Mock implementation for demo
        if model == 'account.move' and method == 'search_read':
            return self._mock_invoices()
        elif model == 'account.account' and method == 'search_read':
            return self._mock_accounts()
        else:
            return []

    def _mock_invoices(self):
        """Mock invoice data for demonstration."""
        return [
            {
                'id': 1,
                'name': 'INV/2026/001',
                'date': '2026-02-01',
                'amount_total': 4500.00,
                'state': 'posted',
                'partner_id': ['Partner 1', 'Client Services Inc.'],
                'invoice_payment_state': 'paid'
            },
            {
                'id': 2,
                'name': 'INV/2026/002',
                'date': '2026-02-08',
                'amount_total': 3200.00,
                'state': 'posted',
                'partner_id': ['Partner 2', 'Tech Solutions LLC'],
                'invoice_payment_state': 'paid'
            },
            {
                'id': 3,
                'name': 'INV/2026/003',
                'date': '2026-02-15',
                'amount_total': 5800.00,
                'state': 'posted',
                'partner_id': ['Partner 3', 'Global Dynamics Corp'],
                'invoice_payment_state': 'not_paid'
            }
        ]

    def _mock_accounts(self):
        """Mock account data for demonstration."""
        return [
            {
                'id': 1,
                'name': '101120 - Accounts Receivable',
                'code': '101120',
                'balance': 5800.00
            },
            {
                'id': 2,
                'name': '400000 - Sales Revenue',
                'code': '400000',
                'balance': 13500.00
            },
            {
                'id': 3,
                'name': '512000 - Operating Expenses',
                'code': '512000',
                'balance': 4200.00
            }
        ]

    def get_revenue_summary(self):
        """Get revenue summary for CEO briefing."""
        invoices = self._call_odoo('account.move', 'search_read')

        total_revenue = sum(inv['amount_total'] for inv in invoices if inv['state'] == 'posted')
        paid_revenue = sum(inv['amount_total'] for inv in invoices if inv['invoice_payment_state'] == 'paid')
        pending_revenue = total_revenue - paid_revenue

        return {
            'total_revenue': total_revenue,
            'paid_revenue': paid_revenue,
            'pending_revenue': pending_revenue,
            'invoice_count': len(invoices),
            'currency': 'USD'
        }

    def get_financial_health(self):
        """Get financial health metrics."""
        accounts = self._call_odoo('account.account', 'search_read')
        revenue_summary = self.get_revenue_summary()

        return {
            'accounts_receivable': 5800.00,
            'revenue': revenue_summary,
            'expenses': 4200.00,
            'net_profit': revenue_summary['paid_revenue'] - 4200.00,
            'profit_margin': (revenue_summary['paid_revenue'] - 4200.00) / revenue_summary['paid_revenue'] if revenue_summary['paid_revenue'] > 0 else 0
        }

    def create_invoice(self, partner_id, amount, description):
        """Create a new invoice (mock)."""
        invoice = {
            'id': 999,
            'name': f'INV/2026/{len(self._mock_invoices()) + 1:03d}',
            'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
            'amount_total': amount,
            'state': 'draft',
            'partner_id': [str(partner_id), 'Customer'],
            'invoice_payment_state': 'not_paid'
        }

        return {
            'success': True,
            'invoice': invoice,
            'message': 'Invoice created successfully (mock)'
        }

    def get_subscription_audit(self):
        """Get subscription and recurring costs."""
        # In production, this would query Odoo's recurring invoicing
        return {
            'subscriptions': [
                {'service': 'Software Licenses', 'amount': 500.00, 'frequency': 'monthly'},
                {'service': 'Cloud Services', 'amount': 200.00, 'frequency': 'monthly'},
                {'service': 'Support Contract', 'amount': 150.00, 'frequency': 'monthly'}
            ],
            'monthly_total': 850.00,
            'annual_total': 10200.00
        }


def main():
    """Test Odoe MCP server."""
    import argparse

    parser = argparse.ArgumentParser(description='Odoo MCP Server')
    parser.add_argument('--revenue', action='store_true',
                       help='Get revenue summary')
    parser.add_argument('--health', action='store_true',
                       help='Get financial health')
    parser.add_argument('--subscriptions', action='store_true',
                       help='Get subscription audit')
    args = parser.parse_args()

    server = OdooMCPServer()

    if args.revenue:
        revenue = server.get_revenue_summary()
        print("\n=== REVENUE SUMMARY ===")
        print(json.dumps(revenue, indent=2))

    if args.health:
        health = server.get_financial_health()
        print("\n=== FINANCIAL HEALTH ===")
        print(json.dumps(health, indent=2))

    if args.subscriptions:
        subs = server.get_subscription_audit()
        print("\n=== SUBSCRIPTION AUDIT ===")
        print(json.dumps(subs, indent=2))

    if not any([args.revenue, args.health, args.subscriptions]):
        parser.print_help()


if __name__ == '__main__':
    main()
