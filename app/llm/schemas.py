"""
app/llm/schemas.py
"""
from pydantic import BaseModel, Field


class PlantOutput(BaseModel):
    """
    Validated shape of an LLM's output
    """
    content: str = Field(
        ...,
        description="The plant's in-character spoken answer or need to express"
    )
