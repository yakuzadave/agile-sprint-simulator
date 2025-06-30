"""
Module simulating individual team member work days and collaboration patterns.
"""

class DailyWorkSimulator:
    def simulate_work_day(self, team_member, assigned_tickets, day):
        """
        Model realistic daily work for a team member.

        :param team_member: TeamMember instance.
        :param assigned_tickets: List of Ticket instances.
        :param day: Day index or date.
        :return: List of log strings for the day.
        """

        logs = []
        logs.append(f"Day {day} | {team_member.name} | Planning and standup")

        for ticket in assigned_tickets:
            if not team_member.can_handle_ticket(ticket):
                logs.append(
                    f"Day {day} | {team_member.name} | Unable to work on {ticket.ticket_id}"
                )
                continue

            logs.append(
                f"Day {day} | {team_member.name} | Started {ticket.ticket_id}: {ticket.description}"
            )

            ticket.status = "In Progress"
            ticket.assigned_to = team_member.name
            effort = team_member.estimate_effort(ticket)
            ticket.actual_effort = effort
            ticket.status = "Closed"
            team_member.current_workload += effort
            team_member.completed_tickets.append(ticket.ticket_id)

            logs.append(
                f"Day {day} | {team_member.name} | Completed {ticket.ticket_id} in {effort} pts"
            )

        logs.append(f"Day {day} | {team_member.name} | Wrap up and documentation")
        return logs
