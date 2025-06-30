"""
Module defining TeamMember model for sprint simulation.
"""
from pydantic import BaseModel, Field
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
    completed_tickets: List[str] = Field(default_factory=list)

    def can_handle_ticket(self, ticket) -> bool:
        """
        Determine if this member can handle the given ticket.
        """
        # Project managers typically don't work tickets directly
        if self.role.lower().startswith("project manager"):
            return False

        # If the ticket category matches one of the member's specialties,
        # we assume they can handle it.
        if ticket.category in self.specialties:
            return True

        # Senior members (skill level >=7) can generally help with any ticket
        return self.skill_level >= 7

    def estimate_effort(self, ticket) -> int:
        """
        Estimate effort (e.g., story points or time) for the ticket.
        """
        base = ticket.estimated_effort or 1

        # Higher skill reduces effort while low availability increases it
        skill_factor = max(0.5, 1.5 - (self.skill_level / 10))
        avail_factor = 1 / self.availability if self.availability > 0 else 2

        effort = int(round(base * skill_factor * avail_factor))
        return max(1, effort)
