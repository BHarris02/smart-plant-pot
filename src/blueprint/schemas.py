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
    image_media_type: str = Field(
        default="image/jpeg",
        description="MIME type of `image`, e.g. image/jpeg or image/png"
    )
    # `image`/`image_media_type` are trusted as-is and forwarded unmodified; the
    # client is responsible for sending a correctly encoded, correctly labeled image


class RunResponse(BaseModel):
    """
    Validate a response to a user `RunRequest`
    """
    status: str = Field(
        ...,
        description="ok"
    )
    content: str | None = Field(
        default=None,
        description="The plant's spoken reply, for clients that want to display it"
    )
