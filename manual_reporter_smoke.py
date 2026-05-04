from agents.reporter import ReportingAgent
from schemas.financial_analysis import FinancialAnalysisSchema
from schemas.research_finding import ResearchFindingSchema

reporter = ReportingAgent()

financial = FinancialAnalysisSchema(
    ticker="AAPL",
    current_price=175.0,
    pe_ratio=28.3,
    analyst_notes="Basic financial metrics based on latest available data."
)


research = [
    ResearchFindingSchema(
        source="Reuters",
        headline="Apple earnings steady",
        summary="Apple reported steady quarterly earnings.",
        relevance_score=0.9,
    )
]

report = reporter.run(
    financial_analysis=financial,
    research_findings=research,
)

print(report)
