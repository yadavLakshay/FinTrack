from pydantic import BaseModel, Field
from typing import Optional


class UserQuerySchema(BaseModel):
    """
    Represents the normalized user intent.
    This is the single source of truth for what the user is asking.
    """

    ticker: str = Field(
        ...,
        description="Stock ticker symbol (e.g., AAPL, TSLA)"
    )

    company_name: Optional[str] = Field(
        None,
        description="Optional full company name provided by the user"
    )

    time_horizon: Optional[str] = Field(
        default="1Y",
        description="Time horizon for analysis (e.g., 1M, 3M, 6M, 1Y)"
    )

    focus: Optional[str] = Field(
        default="fundamental",
        description="Primary analysis focus: fundamental, technical, news, or mixed"
    )
