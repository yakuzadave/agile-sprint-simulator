"""
Module defining Ticket model and TicketGenerator for sprint simulation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
import random


class Ticket(BaseModel):
    """
    Representation of a work ticket.
    """
    ticket_id: str
    source: str  # 'ServiceNow' or 'Jira'
    priority: str  # 'Critical', 'High', 'Medium', 'Low'
    category: str
    description: str
    estimated_effort: Optional[int] = None
    actual_effort: Optional[int] = None
    status: str = 'Open'
    assigned_to: Optional[str] = None
    created_timestamp: Optional[datetime] = None
    completed_timestamp: Optional[datetime] = None
    dependencies: List[str] = Field(default_factory=list)


class TicketGenerator:
    # Default ticket templates by category
    OPERATION_TEMPLATES = [
        {'category': 'Google Workspace', 'description': 'Google Workspace user provisioning/deprovisioning'},
        {'category': 'Email', 'description': 'Email distribution list management'},
        {'category': 'Slack', 'description': 'Slack workspace administration (channels, permissions, integrations)'},
        {'category': 'Adobe Creative Cloud', 'description': 'Adobe Creative Cloud license management'},
        {'category': 'VPN', 'description': 'VPN access issues and certificate renewals'},
        {'category': 'MFA', 'description': 'Multi-factor authentication setup and troubleshooting'},
        {'category': 'File Sharing', 'description': 'File sharing permission escalations'},
        {'category': 'MDM', 'description': 'Mobile device management (MDM) enrollment issues'},
    ]
    INCIDENT_TEMPLATES = [
        {'category': 'Email', 'description': 'Email delivery failures and routing issues'},
        {'category': 'Google Workspace', 'description': 'Google Workspace service outages or performance degradation'},
        {'category': 'Slack', 'description': 'Slack integration failures with third-party tools'},
        {'category': 'Adobe Creative Cloud', 'description': 'Adobe Creative Cloud authentication problems'},
        {'category': 'Network', 'description': 'Network connectivity issues affecting remote workers'},
        {'category': 'Security', 'description': 'Security incidents requiring immediate response'},
        {'category': 'Backup', 'description': 'Data backup and recovery operations'},
    ]
    PROJECT_TEMPLATES = [
        {'category': 'Google Workspace', 'description': 'Implementation of new Google Workspace policies'},
        {'category': 'Slack', 'description': 'Development of custom Slack bots or integrations'},
        {'category': 'Email', 'description': 'Migration project for email systems or user data'},
        {'category': 'Automation', 'description': 'Automation scripts for routine administrative tasks'},
        {'category': 'Infrastructure', 'description': 'Infrastructure upgrades and capacity planning'},
        {'category': 'Compliance', 'description': 'Compliance reporting and audit preparation'},
        {'category': 'Integration', 'description': 'Integration projects between enterprise tools'},
    ]

    # Distribution weights
    MIX_DISTRIBUTION = {'operations': 0.60, 'incidents': 0.25, 'projects': 0.15}
    PRIORITY_LEVELS = ['Critical', 'High', 'Medium', 'Low']
    PRIORITY_WEIGHTS = [0.10, 0.20, 0.50, 0.20]

    def generate_realistic_tickets(self, count, ticket_types=None):
        """
        Generate a set of realistic tickets with mixed categories and priorities.

        :param count: Number of tickets to generate.
        :param ticket_types: Optional dict overriding default templates.
        :return: List of Ticket instances.
        """
        # Allow custom templates or use defaults
        ops_tpl = ticket_types.get('operations', self.OPERATION_TEMPLATES) if ticket_types else self.OPERATION_TEMPLATES
        inc_tpl = ticket_types.get('incidents', self.INCIDENT_TEMPLATES) if ticket_types else self.INCIDENT_TEMPLATES
        proj_tpl = ticket_types.get('projects', self.PROJECT_TEMPLATES) if ticket_types else self.PROJECT_TEMPLATES

        tickets = []
        # Determine counts for each ticket type
        n_ops = int(count * self.MIX_DISTRIBUTION['operations'])
        n_inc = int(count * self.MIX_DISTRIBUTION['incidents'])
        n_proj = count - n_ops - n_inc

        # ID counters
        snw_id = 1000
        jira_id = 2000

        def make_ticket(template, kind):
            nonlocal snw_id, jira_id
            if kind in ('operations', 'incidents'):
                source = 'ServiceNow'
                ticket_id = f'SNW-{snw_id}'
                snw_id += 1
            else:
                source = 'Jira'
                ticket_id = f'JIRA-{jira_id}'
                jira_id += 1

            priority = random.choices(self.PRIORITY_LEVELS, weights=self.PRIORITY_WEIGHTS, k=1)[0]
            category = template['category']
            description = template['description']
            est = self._estimate_effort(kind, priority)

            t = Ticket(
                ticket_id=ticket_id,
                source=source,
                priority=priority,
                category=category,
                description=description,
                estimated_effort=est,
            )
            t.created_timestamp = datetime.now() + timedelta(minutes=random.randint(0, 120))
            return t

        # Generate each bucket
        for _ in range(n_ops):
            tmpl = random.choice(ops_tpl)
            tickets.append(make_ticket(tmpl, 'operations'))
        for _ in range(n_inc):
            tmpl = random.choice(inc_tpl)
            tickets.append(make_ticket(tmpl, 'incidents'))
        for _ in range(n_proj):
            tmpl = random.choice(proj_tpl)
            tickets.append(make_ticket(tmpl, 'projects'))

        # Assign random dependencies (10% chance)
        for t in tickets:
            if random.random() < 0.10:
                dep = random.choice(tickets)
                if dep.ticket_id != t.ticket_id:
                    t.dependencies.append(dep.ticket_id)

        return tickets

    def _estimate_effort(self, kind, priority):
        """
        Estimate story points based on ticket kind and priority.
        """
        # Base ranges by type
        if kind == 'operations':
            base = random.randint(1, 3)
        elif kind == 'incidents':
            base = random.randint(2, 5)
        else:
            base = random.randint(3, 8)

        # Priority bump for urgent work
        if priority == 'Critical':
            base += 2
        elif priority == 'High':
            base += 1

        return base