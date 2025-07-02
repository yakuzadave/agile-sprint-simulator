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


def test_dependency_blocking_and_unblocking():
    team = [
        TeamMember(name="senior", role="Senior", skill_level=8, specialties=["Email"]),
    ]

    t1 = Ticket(ticket_id="SNW-1", source="ServiceNow", priority="High", category="Email", description="First", estimated_effort=2)
    t2 = Ticket(ticket_id="SNW-2", source="ServiceNow", priority="Low", category="Email", description="Second", estimated_effort=2, dependencies=["SNW-1"])

    sim = SprintSimulator(team, sprint_length_days=2)
    sim.sprint_backlog = [t1, t2]
    sim.run_complete_simulation()

    assert t1.status == "Closed"
    assert t2.status == "Closed"
    # Ensure the dependent ticket was blocked at least once
    assert any("blocked" in log.lower() for log in sim.daily_logs)


def test_escalation_flow():
    team = [
        TeamMember(name="junior", role="Junior", skill_level=4, specialties=["Email"]),
        TeamMember(name="senior", role="Senior", skill_level=8, specialties=["Email"]),
    ]

    ticket = Ticket(ticket_id="SNW-3", source="ServiceNow", priority="High", category="Email", description="Hard issue", estimated_effort=6)

    sim = SprintSimulator(team, sprint_length_days=1)
    sim.sprint_backlog = [ticket]
    sim.run_complete_simulation()

    assert ticket.status == "Closed"
    assert ticket.assigned_to == "senior"
    assert any("Escalating" in log for log in sim.daily_logs)
