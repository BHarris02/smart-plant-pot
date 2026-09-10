"""
src/blueprint/api.py
"""
from flask import Blueprint, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from injector import inject

from src.blueprint.schemas import RunRequest, RunResponse
from src.llm import LLMClient
from src.output import OutputMethod
from src.sensor import Sensor, build_sensor_summary


api_bp = Blueprint("api_bp", __name__, url_prefix="/api/v1")
api_spec = FlaskPydanticSpec(backend_name="smart-plant-pot-api", version="1.0.0")

@api_bp.get("/health")
def health():
    """
    health check
    """
    return jsonify({'status': 'healthy'}), 200


@api_bp.post("/run")
@api_spec.validate(
    body=Request(RunRequest),
    resp=Response(HTTP_200=RunResponse)
)
@inject
def run(
    sensors: list[Sensor],
    llm: LLMClient,
    output: OutputMethod
):
    """
    Run the Q&A workflow
    """
    req: RunRequest = request.context.body

    if req.user_question is None:
        output.answer_or_express("Sorry, I didn't catch that.")
        return RunResponse(status="ok").model_dump()

    sensor_summary = build_sensor_summary(sensors)
    plant_output = llm.answer(req.user_question, sensor_summary)
    output.answer_or_express(plant_output.content)
    return RunResponse(status="ok").model_dump()
