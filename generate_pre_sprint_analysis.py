"""
Phase 1: Pre-Sprint Setup and Ticket Generation

Generate the pre-sprint analysis document including a realistic ticket backlog
and a team capacity & skill matrix.
"""

import argparse
from datetime import datetime

from ticket_system import TicketGenerator
from team_members import TeamMember


def build_team():
    """
    Define the default team composition for the sprint simulation.
    """
    return [
        TeamMember(
            name="dev_engineer",
            role="Senior Developer/DevOps Engineer",
            skill_level=9,
            specialties=["Python", "Java", "Infrastructure Automation"],
        ),
        TeamMember(
            name="senior_syseng",
            role="Senior Information Systems Engineer",
            skill_level=8,
            specialties=["Google Workspace", "Email Architecture", "Authentication Systems"],
        ),
        TeamMember(
            name="junior_syseng_tech",
            role="Junior Information Systems Engineer (Technical)",
            skill_level=5,
            specialties=[
                "Java",
                "Python",
                "Slack Administration",
                "Email Support",
                "Adobe Enterprise License Management",
            ],
        ),
        TeamMember(
            name="junior_syseng_a",
            role="Junior Information Systems Engineer A",
            skill_level=4,
            specialties=["User Provisioning", "Permissions Management", "Documentation"],
        ),
        TeamMember(
            name="junior_syseng_b",
            role="Junior Information Systems Engineer B",
            skill_level=4,
            specialties=[
                "Hardware/Software Inventory",
                "Network Troubleshooting",
                "User Training",
                "Compliance Support",
            ],
        ),
        TeamMember(
            name="project_manager",
            role="Project Manager",
            skill_level=7,
            specialties=[
                "Sprint Planning",
                "Backlog Management",
                "Stakeholder Communication",
                "Risk Management",
            ],
            availability=0.8,
        ),
    ]


def format_tickets(tickets):
    header = (
        "| Ticket ID | Source | Priority | Category | Est Effort | Dependencies | Description |"
    )
    sep = "|---|---|---|---|---|---|---|"
    lines = [header, sep]
    for t in tickets:
        deps = ",".join(t.dependencies) if t.dependencies else ""
        lines.append(
            f"| {t.ticket_id} | {t.source} | {t.priority} | {t.category} | "
            f"{t.estimated_effort} | {deps} | {t.description} |"
        )
    return "\n".join(lines)


def format_team(team):
    header = "| Name | Role | Skill Level | Specialties | Availability |"
    sep = "|---|---|---|---|---|"
    lines = [header, sep]
    for m in team:
        specs = ", ".join(m.specialties)
        lines.append(
            f"| {m.name} | {m.role} | {m.skill_level} | {specs} | {m.availability} |"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate pre-sprint analysis document (Phase 1)."
    )
    parser.add_argument(
        "-n", "--num-tickets", type=int, default=20,
        help="Number of tickets to generate."
    )
    parser.add_argument(
        "-o", "--output", default="pre_sprint_analysis.md",
        help="Output markdown file name."
    )
    args = parser.parse_args()

    team = build_team()
    tickets = TicketGenerator().generate_realistic_tickets(args.num_tickets)

    total_availability = sum(m.availability for m in team)
    team_size = len(team)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(args.output, "w") as f:
        f.write("# Pre-Sprint Analysis\n\n")
        f.write(f"_Generated on {now}_\n\n")
        f.write("## Ticket Backlog\n\n")
        f.write(format_tickets(tickets) + "\n\n")
        f.write("## Team Capacity & Skill Matrix\n\n")
        f.write(format_team(team) + "\n\n")
        f.write("## Capacity Planning\n\n")
        f.write(
            f"- Team size: {team_size} members  \n"
            f"- Total availability: {total_availability:.1f} FTE\n\n"
        )
        f.write("## Triage Meeting Notes\n\n")
        f.write("_To be captured in Phase 2_\n\n")
        f.write("## Sprint Commitment & Goals\n\n")
        f.write("_To be captured in Phase 2_\n")


if __name__ == "__main__":
    main()
