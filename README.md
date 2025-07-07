# Sprint Simulator

This repository provides a Python-based simulation of an IT operations/development team sprint cycle,
including realistic ticket generation, team capacity modeling, and planning/execution workflows.

## Phase 1: Pre-Sprint Analysis

Generate a pre-sprint analysis document containing the ticket backlog and team capacity/skill matrix:
```bash
python generate_pre_sprint_analysis.py --num-tickets 20 --output pre_sprint_analysis.md
```

## Setup

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running Tests

Install `pytest` and run the test suite:

```bash
pip install pytest
pytest
```

Further phases (sprint planning, daily simulation, retrospective) will be added following the specification in AGENTS.md.

## Metrics Generation

After running a simulation you can generate a structured metrics report:

```python
from ticket_system import TicketGenerator
from sprint_simulator import SprintSimulator
from team_members import TeamMember

team = [TeamMember(name="dev", role="Developer", skill_level=8, specialties=["Email"])]
tickets = TicketGenerator().generate_realistic_tickets(5)
sim = SprintSimulator(team, sprint_length_days=1)
sim.sprint_backlog = tickets
sim.run_complete_simulation()
metrics = sim.generate_metrics_report()
sim.save_metrics_report("metrics.json")
```

This will save `metrics.json` containing velocity and completion statistics for the sprint.

## Specification

Refer to `AGENTS.md` for the full project requirements and roadmap.
