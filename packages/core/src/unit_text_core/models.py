from pydantic import BaseModel


class IdeaModel(BaseModel):
    """Represents an idea for a piece of writing."""

    topic: str | None
    audience: str | None
    audience_knowledge: str | None
    audience_care: str | None
    desired_action: str | None
    goal: str | None
    perspective: str | None


class Evaluation(BaseModel):
    """The evaluation and suggestions for a specific aspect of a piece of writing."""

    evaluation: str
    suggestions: str
    test_passed: bool


class TestResult(BaseModel):
    """The results of a test on a piece of writing."""

    clarity: Evaluation
    alignment_with_objectives: Evaluation
    completeness: Evaluation
    overall_suggestions: str
