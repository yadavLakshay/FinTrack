from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class ResearchFindingSchema(BaseModel):
    """
    Represents a single research finding produced by the Researcher Agent
    and stored in shared memory.
    """

    ticker: str = Field(
        ...,
        description="Stock ticker the finding relates to"
    )

    source: str = Field(
        ...,
        description="News source or website name"
    )

    headline: str = Field(
        ...,
        description="Headline or title of the article"
    )

    summary: str = Field(
        ...,
        description="Concise summary of the relevant content"
    )

    published_date: Optional[date] = Field(
        None,
        description="Publication date of the source content"
    )

    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Agent-estimated relevance score between 0 and 1"
    )

    tags: List[str] = Field(
        default_factory=list,
        description="Tags such as earnings, macro, product, legal, etc."
    )
