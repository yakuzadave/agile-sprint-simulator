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

        assignments = {member.name: [] for member in self.team}

        for ticket in self.sprint_backlog:
            if ticket.status != "Open":
                continue
            for member in self.team:
                if member.can_handle_ticket(ticket):
                    assignments[member.name].append(ticket)
                    ticket.status = "Assigned"
                    break

        for member in self.team:
            tickets = assignments[member.name]
            if not tickets:
                continue
            logs = DailyWorkSimulator().simulate_work_day(member, tickets, day)
            self.daily_logs.extend(logs)

        for ticket in list(self.sprint_backlog):
            if ticket.status == "Closed":
                self.sprint_backlog.remove(ticket)
                self.completed_work.append(ticket)
