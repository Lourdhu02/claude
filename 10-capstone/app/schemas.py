"""Pydantic schemas for the capstone Research Assistant."""

from pydantic import BaseModel, Field


class Citation(BaseModel):
    source: str = Field(description="URL or document title.")
    quote: str = Field(description="A short verbatim quote backing the claim.")


class Report(BaseModel):
    question: str
    answer: str = Field(description="One-paragraph direct answer.")
    bullets: list[str] = Field(description="3-5 key findings, each one sentence.")
    citations: list[Citation] = Field(description="Every claim should have at least one citation.")
    confidence: str = Field(description="low | medium | high")


# Used as the forced-tool schema for the orchestrator's final output.
REPORT_TOOL = {
    "name": "deliver_report",
    "description": "Deliver the final research report. Call exactly once when investigation is complete.",
    "input_schema": Report.model_json_schema(),
}
