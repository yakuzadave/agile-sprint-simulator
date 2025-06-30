import random
from collections import Counter

from ticket_system import TicketGenerator


def test_ticket_type_distribution():
    random.seed(0)
    gen = TicketGenerator()
    tickets = gen.generate_realistic_tickets(20)

    counts = Counter(t.source for t in tickets)

    # Operations and incidents use ServiceNow
    expected_snw = int(20 * (
        TicketGenerator.MIX_DISTRIBUTION['operations'] +
        TicketGenerator.MIX_DISTRIBUTION['incidents']
    ))
    assert counts['ServiceNow'] == expected_snw
    assert counts['Jira'] == 20 - expected_snw


def test_priority_distribution():
    random.seed(42)
    gen = TicketGenerator()
    tickets = gen.generate_realistic_tickets(1000)
    counts = Counter(t.priority for t in tickets)

    for level, weight in zip(TicketGenerator.PRIORITY_LEVELS, TicketGenerator.PRIORITY_WEIGHTS):
        proportion = counts[level] / 1000
        assert abs(proportion - weight) < 0.05

