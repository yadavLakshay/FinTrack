from schemas.user_query import UserQuerySchema
from schemas.agent_task import AgentTaskSchema
from schemas.final_report import FinalReportSchema

from agents.researcher import conduct_research
from agents.analyst import perform_analysis
from agents.reporter import generate_report


def orchestrate_workflow(query: UserQuerySchema) -> FinalReportSchema:
    """
    Orchestrates the full workflow:
    Researcher → Analyst → Reporter.
    """
    ticker = query.ticker

    # --- Researcher Task ---
    research_task = AgentTaskSchema(
        agent_role="researcher",
        task_objective="Fetch recent news and sentiment",
        ticker=ticker,
    )

    conduct_research(research_task)

    # --- Analyst Task ---
    analyst_task = AgentTaskSchema(
        agent_role="analyst",
        task_objective="Analyze financial performance",
        ticker=ticker,
    )

    perform_analysis(analyst_task)

    # --- Reporter ---
    final_report = generate_report(ticker)

    return final_report
