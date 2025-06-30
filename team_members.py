"""
Module defining TeamMember model for sprint simulation.
"""
from pydantic import BaseModel
from typing import List


class TeamMember(BaseModel):
    """
    Representation of a team member and their capabilities.
    """
    name: str
    role: str
    skill_level: int  # 1-10 scale
    specialties: List[str]
    availability: float = 1.0  # fraction of capacity (0.0-1.0)
    current_workload: int = 0
    completed_tickets: List[str] = []

    def can_handle_ticket(self, ticket) -> bool:
        """
        Determine if this member can handle the given ticket.
        """
        raise NotImplementedError

    def estimate_effort(self, ticket) -> int:
        """
        Estimate effort (e.g., story points or time) for the ticket.
        """
        raise NotImplementedError