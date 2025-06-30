import unittest
from team_members import TeamMember
from ticket_system import Ticket
from sprint_simulator import SprintSimulator

class TestSprintSimulation(unittest.TestCase):
    def test_basic_run(self):
        team = [
            TeamMember(name="dev", role="Developer", skill_level=8, specialties=["Email", "Slack"]),
            TeamMember(name="junior", role="Junior", skill_level=5, specialties=["Email"]),
        ]

        tickets = [
            Ticket(ticket_id="SNW-1", source="ServiceNow", priority="High", category="Email", description="Email issue", estimated_effort=3),
            Ticket(ticket_id="SNW-2", source="ServiceNow", priority="Low", category="Slack", description="Slack request", estimated_effort=2),
        ]

        sim = SprintSimulator(team, sprint_length_days=1)
        sim.sprint_backlog = tickets
        logs = sim.run_complete_simulation()

        self.assertEqual(len(sim.completed_work), 2)
        for t in tickets:
            self.assertEqual(t.status, "Closed")
        self.assertTrue(len(logs) > 0)

if __name__ == "__main__":
    unittest.main()
