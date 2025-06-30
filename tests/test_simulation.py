from team_members import TeamMember
from ticket_system import Ticket
from sprint_simulator import SprintSimulator


def test_basic_run():
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

    assert len(sim.completed_work) == 2
    for t in tickets:
        assert t.status == "Closed"
    assert len(logs) > 0
