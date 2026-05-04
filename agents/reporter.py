from typing import List
from openai import OpenAI
from pydantic import ValidationError

from schemas.financial_analysis import FinancialAnalysisSchema
from schemas.research_finding import ResearchFindingSchema
from schemas.final_report import FinalReportSchema


class ReportingAgent:
    """
    Step 3.1: LLM-backed reporting agent.
    Input: schemas only
    Output: FinalReportSchema only
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def run(
        self,
        financial_analysis: FinancialAnalysisSchema | None,
        research_findings: List[ResearchFindingSchema],
    ) -> FinalReportSchema:

        system_prompt = (
            "You are a reporting agent in a financial analysis system.\n\n"
            "STRICT RULES:\n"
            "- Use ONLY the provided structured input data.\n"
            "- Do NOT compute, infer, estimate, or derive any numbers.\n"
            "- Do NOT introduce numeric values not explicitly present.\n"
            "- Use numbers verbatim exactly as provided.\n"
            "- If a value is missing, omit commentary.\n"
            "- Output MUST be valid JSON matching FinalReportSchema exactly.\n"
            "- Do NOT include markdown, explanations, or extra text.\n"
        )

        user_payload = {
            "financial_analysis": (
                financial_analysis.model_dump() if financial_analysis else None
            ),
            "research_findings": [r.model_dump() for r in research_findings],
            "output_schema": "FinalReportSchema",
        }

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(user_payload)},
            ],
            temperature=0.0,
        )

        raw_output = response.choices[0].message.content

        try:
            return FinalReportSchema.model_validate_json(raw_output)
        except ValidationError as e:
            raise RuntimeError(
                "Reporter produced invalid FinalReportSchema output"
            ) from e
