"""
src/module/output.py
"""
from injector import Module, provider, singleton

from src.output import OutputMethod
# temp: remove before packaging for production
from src.output import LaptopSpeakerOutputMethod


class OutputModule(Module):
    """
    DI module for `OutputMethod`s
    """
    @provider
    @singleton
    def provide_output_method(self) -> OutputMethod:
        """
        Provide a concrete `OutputMethod`
        """
        return LaptopSpeakerOutputMethod()
