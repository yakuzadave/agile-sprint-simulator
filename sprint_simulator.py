"""
Module implementing the SprintSimulator, orchestrating end-to-end sprint flow.
"""

class SprintSimulator:
    def __init__(self, team, sprint_length_days=10):
        """
        Initialize the sprint simulation.

        :param team: List of TeamMember instances.
        :param sprint_length_days: Sprint length in business days.
        """
        self.team = team
        self.sprint_length = sprint_length_days
        self.current_day = 0
        self.sprint_backlog = []
        self.completed_work = []
        self.daily_logs = []

    def run_complete_simulation(self):
        """
        Run the full sprint simulation end-to-end.
        """
        for day in range(1, self.sprint_length + 1):
            self.current_day = day
            self.simulate_daily_standup(day)
            self.simulate_work_day(day)

        return self.daily_logs

    def simulate_daily_standup(self, day):
        """
        Simulate the daily standup meeting content.
        :param day: Day index.
        """
        lines = [f"Day {day} Standup"]
        for member in self.team:
            lines.append(
                f"- {member.name}: {len(member.completed_tickets)} tickets completed"
            )
        self.daily_logs.append("\n".join(lines))

    def simulate_work_day(self, day):
        """
        Simulate the activities of a single work day.
        :param day: Day index.
        """
        from daily_work_simulator import DailyWorkSimulator

        work_sim = DailyWorkSimulator()

        ticket_lookup = {t.ticket_id: t for t in self.sprint_backlog + self.completed_work}

        assignments = {member.name: [] for member in self.team}

        for ticket in self.sprint_backlog:
            if ticket.status == "Closed":
                continue

            if ticket.dependencies:
                unresolved = [
                    dep for dep in ticket.dependencies
                    if ticket_lookup.get(dep) and ticket_lookup[dep].status != "Closed"
                ]
                if unresolved:
                    ticket.status = "Blocked"
                    self.daily_logs.append(
                        f"Day {day} | {ticket.ticket_id} blocked waiting for {','.join(unresolved)}"
                    )
                    continue
                else:
                    if ticket.status == "Blocked":
                        ticket.status = "Open"

            if ticket.status != "Open":
                continue

            for member in self.team:
                if member.can_handle_ticket(ticket):
                    assignments[member.name].append(ticket)
                    ticket.status = "Assigned"
                    break

        escalated_assignments = {member.name: [] for member in self.team}

        for member in self.team:
            tickets = assignments[member.name]
            if not tickets:
                continue
            logs, escalated = work_sim.simulate_work_day(member, tickets, day, ticket_lookup)
            self.daily_logs.extend(logs)

            for t in escalated:
                for senior in self.team:
                    if senior.skill_level >= 7 and senior.can_handle_ticket(t):
                        escalated_assignments[senior.name].append(t)
                        break

        for member in self.team:
            tickets = escalated_assignments[member.name]
            if not tickets:
                continue
            logs, _ = work_sim.simulate_work_day(member, tickets, day, ticket_lookup)
            self.daily_logs.extend(logs)

        for ticket in list(self.sprint_backlog):
            if ticket.status == "Closed":
                self.sprint_backlog.remove(ticket)
                self.completed_work.append(ticket)
