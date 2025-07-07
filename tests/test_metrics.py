from team_members import TeamMember
from ticket_system import Ticket
from sprint_simulator import SprintSimulator


def test_metrics_generation():
    team = [TeamMember(name="dev", role="Developer", skill_level=8, specialties=["Email"])]
    ticket = Ticket(ticket_id="SNW-1", source="ServiceNow", priority="High", category="Email", description="Issue", estimated_effort=3)
    sim = SprintSimulator(team, sprint_length_days=1)
    sim.sprint_backlog = [ticket]
    sim.run_complete_simulation()
    metrics = sim.generate_metrics_report()

    assert metrics["completed_tickets"] == 1
    assert metrics["velocity"] > 0
    assert metrics["utilization"]["dev"] > 0
