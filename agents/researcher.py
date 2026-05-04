import yfinance as yf
from datetime import datetime

from schemas.agent_task import AgentTaskSchema
from schemas.research_finding import ResearchFindingSchema
from memory.vector_store import store_research_finding


def conduct_research(task: AgentTaskSchema) -> list[ResearchFindingSchema]:
    """
    Conducts research based on the given task.
    Fetches recent news related to the ticker and stores findings in memory.
    """
    ticker = task.ticker
    stock = yf.Ticker(ticker)

    findings: list[ResearchFindingSchema] = []

    news_items = stock.news or []

    for item in news_items[:5]:
        headline = item.get("title", "")
        source = item.get("publisher", "Unknown")

        finding = ResearchFindingSchema(
            ticker=ticker,
            source=source,
            headline=headline,
            summary=headline,  # simple safe summary for now
            published_date=datetime.fromtimestamp(
                item.get("providerPublishTime", 0)
            ).date()
            if item.get("providerPublishTime")
            else None,
            relevance_score=0.8,
            tags=["news"],
        )

        store_research_finding(finding)
        findings.append(finding)

    return findings
