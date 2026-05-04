from pydantic import BaseModel, Field
from typing import List


class FinalReportSchema(BaseModel):
    """
    Represents the final synthesized financial report
    delivered to the end user.
    """

    ticker: str = Field(
        ...,
        description="Stock ticker symbol"
    )

    executive_summary: str = Field(
        ...,
        description="High-level executive summary (<=150 words)"
    )

    company_snapshot: str = Field(
        ...,
        description="Brief overview of the company and its market position"
    )

    key_financials: List[str] = Field(
        ...,
        description="Bullet-point financial highlights"
    )

    recent_news: List[str] = Field(
        ...,
        description="Summarized recent news points"
    )

    opportunities: List[str] = Field(
        ...,
        description="Potential upside factors"
    )

    risks: List[str] = Field(
        ...,
        description="Key risk factors"
    )

    final_outlook: str = Field(
        ...,
        description="Overall analytical conclusion"
    )

    disclaimer: str = Field(
        default="This report is AI-generated and not financial advice.",
        description="Mandatory disclaimer"
    )
