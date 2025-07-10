from team_members import TeamMember
from ticket_system import Ticket
from sprint_planning import simulate_triage_meeting


def test_triage_prioritization_and_commitment():
    team = [TeamMember(name="dev", role="Developer", skill_level=8, specialties=["Email"])]
    t1 = Ticket(ticket_id="SNW-1", source="ServiceNow", priority="Critical", category="Email", description="A", estimated_effort=3)
    t2 = Ticket(ticket_id="SNW-2", source="ServiceNow", priority="Low", category="Email", description="B", estimated_effort=2, dependencies=["SNW-1"])

    notes, commit = simulate_triage_meeting([t2, t1], team)

    commit_lines = [l for l in commit.splitlines() if l.startswith("|")]
    assert commit_lines[2].split("|")[1].strip() == "SNW-1"
    assert "Estimated velocity" in commit
    assert "capacity" in notes.lower()
