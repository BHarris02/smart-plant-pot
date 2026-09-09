"""
app/policy/services.py
"""
from app.policy.models import Need
from app.policy.need import NeedPolicy
from app.sensor import SensorReading


class NeedEvaluatorService:
    """
    Runs a `NeedPolicy` per metric against current sensor readings
    """
    def __init__(self, policies: list[NeedPolicy]):
        self._policies = {policy.metric: policy for policy in policies}

    def evaluate(self, readings: dict[str, SensorReading]) -> list[Need]:
        """
        Evaulate each sensor reading against their respective policy
        """
        needs = []
        for metric, reading in readings.items():
            policy = self._policies.get(metric)
            if policy:
                need = policy.evaluate(reading)
                if need:
                    needs.append(need)
        return needs
