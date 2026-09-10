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


class RunResponse(BaseModel):
    """
    Validate a response to a user `RunRequest`
    """
    status: str = Field(
        ...,
        description="ok"
    )
