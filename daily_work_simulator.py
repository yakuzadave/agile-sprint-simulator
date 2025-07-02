"""
Module simulating individual team member work days and collaboration patterns.
"""

class DailyWorkSimulator:
    """Simulate work for individual team members."""

    ESCALATION_THRESHOLD = 5

    def simulate_work_day(self, team_member, assigned_tickets, day, ticket_lookup=None):
        """
        Model realistic daily work for a team member.

        :param team_member: TeamMember instance.
        :param assigned_tickets: List of Ticket instances.
        :param day: Day index or date.
        :return: List of log strings for the day.
        """

        logs = []
        escalated = []
        logs.append(f"Day {day} | {team_member.name} | Planning and standup")

        for ticket in assigned_tickets:
            if not team_member.can_handle_ticket(ticket):
                logs.append(
                    f"Day {day} | {team_member.name} | Unable to work on {ticket.ticket_id}"
                )
                continue

            # Check for unresolved dependencies
            if ticket_lookup and ticket.dependencies:
                unresolved = [
                    dep
                    for dep in ticket.dependencies
                    if ticket_lookup.get(dep) and ticket_lookup[dep].status != "Closed"
                ]
                if unresolved:
                    ticket.status = "Blocked"
                    logs.append(
                        f"Day {day} | {team_member.name} | Blocked on {ticket.ticket_id} waiting for {','.join(unresolved)}"
                    )
                    continue

            logs.append(
                f"Day {day} | {team_member.name} | Started {ticket.ticket_id}: {ticket.description}"
            )

            ticket.status = "In Progress"
            ticket.assigned_to = team_member.name
            effort = team_member.estimate_effort(ticket)

            if team_member.skill_level < 6 and effort > self.ESCALATION_THRESHOLD:
                ticket.status = "Open"
                ticket.assigned_to = None
                logs.append(
                    f"Day {day} | {team_member.name} | Escalating {ticket.ticket_id} to senior engineer"
                )
                escalated.append(ticket)
                continue

            ticket.actual_effort = effort
            ticket.status = "Closed"
            team_member.current_workload += effort
            team_member.completed_tickets.append(ticket.ticket_id)

            logs.append(
                f"Day {day} | {team_member.name} | Completed {ticket.ticket_id} in {effort} pts"
            )

        logs.append(f"Day {day} | {team_member.name} | Wrap up and documentation")
        return logs, escalated
