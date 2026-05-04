from pydantic import BaseModel, Field
from typing import Optional


class FinancialAnalysisSchema(BaseModel):
    """
    Represents structured financial analysis produced by the Analyst Agent
    and stored in shared memory.
    """

    ticker: str = Field(
        ...,
        description="Stock ticker symbol"
    )

    price_current: Optional[float] = Field(
        None,
        description="Current stock price"
    )

    price_change_pct: Optional[float] = Field(
        None,
        description="Percentage price change over the selected horizon"
    )

    pe_ratio: Optional[float] = Field(
        None,
        description="Price-to-Earnings ratio"
    )

    roe: Optional[float] = Field(
        None,
        description="Return on Equity"
    )

    debt_to_equity: Optional[float] = Field(
        None,
        description="Debt-to-Equity ratio"
    )

    revenue_growth_yoy: Optional[float] = Field(
        None,
        description="Year-over-year revenue growth"
    )

    eps_growth_yoy: Optional[float] = Field(
        None,
        description="Year-over-year EPS growth"
    )

    volatility: Optional[float] = Field(
        None,
        description="Estimated price volatility"
    )

    analyst_notes: str = Field(
        ...,
        description="Plain-English interpretation of the financial metrics"
    )
