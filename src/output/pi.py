"""
src/output/pi.py
"""
import subprocess

from src.output.api import OutputMethod


class PiSpeakerOutputMethod(OutputMethod):
    """
    Concrete `OutputMethod` that speaks text aloud via the Pi's speakers.
    Uses espeak-ng (free, local, offline, FR-05)
    """
    def answer_or_express(self, content: str) -> None:
        # list-form args avoid shell injection since content may come from LLM output
        subprocess.run(["espeak-ng", content], check=True)
