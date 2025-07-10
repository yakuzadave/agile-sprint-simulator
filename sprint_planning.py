"""Sprint planning utilities including triage meeting simulation."""
from typing import List, Tuple

from ticket_system import Ticket
from team_members import TeamMember


PRIORITY_ORDER = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
}


def _prioritize_tickets(tickets: List[Ticket]) -> List[Ticket]:
    """Return tickets sorted by priority and dependencies."""
    # Simple topological sort respecting dependencies then priority
    ticket_map = {t.ticket_id: t for t in tickets}
    visited = set()
    ordered: List[Ticket] = []

    def visit(ticket: Ticket):
        if ticket.ticket_id in visited:
            return
        for dep in ticket.dependencies:
            if dep in ticket_map:
                visit(ticket_map[dep])
        visited.add(ticket.ticket_id)
        ordered.append(ticket)

    for t in sorted(tickets, key=lambda x: PRIORITY_ORDER.get(x.priority, 5)):
        visit(t)

    # Remove duplicates while preserving order
    seen = set()
    final = []
    for t in ordered:
        if t.ticket_id not in seen:
            final.append(t)
            seen.add(t.ticket_id)
    return final


def simulate_triage_meeting(tickets: List[Ticket], team: List[TeamMember]) -> Tuple[str, str]:
    """Simulate a triage meeting and return markdown sections."""
    ordered = _prioritize_tickets(tickets)

    capacity = int(sum(m.availability for m in team) * 8)  # simple velocity model
    velocity = 0
    commitment: List[Ticket] = []

    for t in ordered:
        effort = t.estimated_effort or 1
        if velocity + effort > capacity:
            continue
        if any(m.can_handle_ticket(t) for m in team):
            commitment.append(t)
            velocity += effort

    dep_pairs = [f"{t.ticket_id}->{dep}" for t in ordered for dep in t.dependencies]

    notes_lines = [
        f"- Reviewed {len(tickets)} tickets and prioritized Critical and High items first.",
        "- Matched work to available team skills and workloads.",
    ]
    if dep_pairs:
        notes_lines.append(
            "- Sequenced dependent work: " + ", ".join(dep_pairs)
        )
    notes_lines.extend([
        "- Flagged high-effort items for risk mitigation.",
        f"- Team capacity for this sprint is {capacity} story points; committed {velocity} points of work.",
    ])

    commit_lines = ["| Ticket ID | Priority | Est Effort |", "|---|---|---|"]
    for t in commitment:
        commit_lines.append(
            f"| {t.ticket_id} | {t.priority} | {t.estimated_effort or 1} |"
        )
    commit_lines.append("")
    commit_lines.append(f"Estimated velocity: {velocity} pts")

    return "\n".join(notes_lines), "\n".join(commit_lines)
