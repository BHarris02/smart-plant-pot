"""
src/blueprint/schemas.py
"""
from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    """
    Validate a user request to run the application once
    """
    user_question: str = Field(
        ...,
        description="The user's question transcribed"
    )
    image: str | None = Field(
        default=None,
        description="Optional photo of the plant, pre-encoded as base64 by the client"
    )


class RunResponse(BaseModel):
    """
    Validate a response to a user `RunRequest`
    """
    content: str = Field(
        ...,
        description="The LLM's response for display on the frontend client"
    )
