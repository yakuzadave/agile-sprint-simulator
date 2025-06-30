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

## Specification

Refer to `AGENTS.md` for the full project requirements and roadmap.
