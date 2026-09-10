"""
api/src/blueprint/schemas.py
"""
from pydantic import BaseModel, Field


class TranscribeRequest(BaseModel):
    """
    Validates a request to transcribe raw audio bytes
    """
    audio_bytes: bytes = Field(..., description="Raw audio bytes")


class TranscribeResponse(BaseModel):
    """
    Validates transcribe response
    """
    text: str = Field(..., description="Transcribed text")
