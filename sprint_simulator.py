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
        self.metrics = {}

    def run_complete_simulation(self):
        """
        Run the full sprint simulation end-to-end.
        """
        for day in range(1, self.sprint_length + 1):
            self.current_day = day
            self.simulate_daily_standup(day)
            self.simulate_work_day(day)

        # Capture metrics at the end of the simulation
        self.metrics = self.generate_metrics_report()
        return self.daily_logs

    def generate_metrics_report(self):
        """Generate performance metrics for the completed sprint."""
        from collections import Counter

        metrics = {}
        backlog_total = len(self.completed_work) + len(self.sprint_backlog)
        metrics["total_tickets"] = backlog_total
        metrics["completed_tickets"] = len(self.completed_work)

        velocity = sum(
            (t.actual_effort or t.estimated_effort or 0) for t in self.completed_work
        )
        metrics["velocity"] = velocity

        metrics["completed_by_priority"] = dict(
            Counter(t.priority for t in self.completed_work)
        )
        metrics["completed_by_category"] = dict(
            Counter(t.category for t in self.completed_work)
        )
        metrics["utilization"] = {m.name: m.current_workload for m in self.team}
        metrics["escalations"] = len(
            [log for log in self.daily_logs if "Escalating" in log]
        )
        return metrics

    def save_metrics_report(self, path):
        """Persist metrics as a JSON document."""
        import json

        if not self.metrics:
            self.metrics = self.generate_metrics_report()

        with open(path, "w") as f:
            json.dump(self.metrics, f, indent=2)

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
