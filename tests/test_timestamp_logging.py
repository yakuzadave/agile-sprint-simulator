from datetime import datetime

from daily_work_simulator import DailyWorkSimulator
from team_members import TeamMember
from ticket_system import Ticket


def test_business_hours_timestamps():
    member = TeamMember(name="dev", role="Developer", skill_level=8, specialties=["Email"])
    ticket = Ticket(ticket_id="SNW-1", source="ServiceNow", priority="Low", category="Email", description="Issue", estimated_effort=1)
    sim = DailyWorkSimulator()
    logs, _ = sim.simulate_work_day(member, [ticket], day=1)

    for line in logs:
        ts_str, _ = line.split(" | ", 1)
        dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        assert 8 <= dt.hour <= 18


def test_after_hours_entry_present_for_critical():
    member = TeamMember(name="dev", role="Developer", skill_level=8, specialties=["Email"])
    ticket = Ticket(ticket_id="SNW-2", source="ServiceNow", priority="Critical", category="Email", description="Big issue", estimated_effort=1)
    sim = DailyWorkSimulator()
    logs, _ = sim.simulate_work_day(member, [ticket], day=1)

    times = [datetime.strptime(line.split(" | ", 1)[0], "%Y-%m-%d %H:%M:%S") for line in logs]
    assert any(t.time() > datetime.strptime("18:00:00", "%H:%M:%S").time() for t in times)
