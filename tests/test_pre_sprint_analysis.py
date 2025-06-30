import subprocess
import sys


def test_pre_sprint_analysis_output(tmp_path):
    out_file = tmp_path / "analysis.md"
    subprocess.run(
        [sys.executable, "generate_pre_sprint_analysis.py", "--num-tickets", "5", "--output", str(out_file)],
        check=True,
    )

    content = out_file.read_text()
    assert "# Pre-Sprint Analysis" in content
    assert "## Ticket Backlog" in content
    assert "## Team Capacity & Skill Matrix" in content

    ticket_lines = [
        line
        for line in content.splitlines()
        if line.startswith("| SNW-") or line.startswith("| JIRA-")
    ]
    assert len(ticket_lines) == 5
