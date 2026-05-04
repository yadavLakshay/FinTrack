import yfinance as yf
import pandas as pd
import numpy as np

from schemas.agent_task import AgentTaskSchema
from schemas.financial_analysis import FinancialAnalysisSchema
from memory.vector_store import store_financial_analysis


def perform_analysis(task: AgentTaskSchema) -> FinancialAnalysisSchema:
    """
    Performs financial analysis on the given ticker and stores the result in memory.
    """
    ticker = task.ticker
    stock = yf.Ticker(ticker)

    # Fetch price history (1Y)
    hist = stock.history(period="1y")

    price_current = None
    price_change_pct = None
    volatility = None

    if not hist.empty:
        price_current = float(hist["Close"].iloc[-1])
        price_start = float(hist["Close"].iloc[0])
        price_change_pct = (price_current - price_start) / price_start

        returns = hist["Close"].pct_change().dropna()
        volatility = float(returns.std())

    # Fetch fundamental info
    info = stock.info or {}

    pe_ratio = info.get("trailingPE")
    roe = info.get("returnOnEquity")
    debt_to_equity = info.get("debtToEquity")

    analysis = FinancialAnalysisSchema(
        ticker=ticker,
        price_current=price_current,
        price_change_pct=price_change_pct,
        pe_ratio=pe_ratio,
        roe=roe,
        debt_to_equity=debt_to_equity,
        revenue_growth_yoy=None,
        eps_growth_yoy=None,
        volatility=volatility,
        analyst_notes="Basic financial metrics computed from recent market data."
    )

    store_financial_analysis(analysis)

    return analysis
