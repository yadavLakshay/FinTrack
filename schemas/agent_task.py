from pydantic import BaseModel, Field
from typing import Literal, Optional


class AgentTaskSchema(BaseModel):
    """
    Represents a task delegated by the Manager Agent
    to a specialized worker agent.
    """

    agent_role: Literal["researcher", "analyst", "reporter"] = Field(
        ...,
        description="Target agent responsible for executing the task"
    )

    task_objective: str = Field(
        ...,
        description="Clear and specific task objective for the agent"
    )

    ticker: str = Field(
        ...,
        description="Stock ticker symbol the task applies to"
    )

    constraints: Optional[str] = Field(
        None,
        description="Optional hard constraints the agent must follow"
    )
