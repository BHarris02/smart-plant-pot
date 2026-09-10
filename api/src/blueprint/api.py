"""
api/src/blueprints.py
"""
from flask import Blueprint, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from injector import inject

from src.blueprint.schemas import TranscribeRequest, TranscribeResponse
from src.service import InputTranscriber


api_bp = Blueprint("api_bp", __name__, url_prefix="/api/v1")
api_spec = FlaskPydanticSpec(backend_name="smart-plant-pot-api", version="1.0.0")

@api_bp.get("/health")
def health():
    """
    health check
    """
    return jsonify({'status': 'healthy'}), 200


@api_bp.post("/transcribe")
@api_spec.validate(
    body=Request(TranscribeRequest),
    resp=Response(HTTP_200=TranscribeResponse)
)
@inject
def transcribe(input_transcriber: InputTranscriber):
    """
    Transcribe raw audio bytes
    """
    audio_file = request.files.get("file")
    if audio_file is None:
        return jsonify({"error": "missing 'file' in multipart form data"}), 400

    text = input_transcriber.transcribe(audio_file.read())
    return TranscribeResponse(text=text).model_dump()
