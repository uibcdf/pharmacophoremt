from abc import ABC, abstractmethod
from argdigest import arg_digest
from smonitor import signal

class Modeler(ABC):
    """Base class for all pharmacophore modelers."""

    @abstractmethod
    def build(self, **kwargs):
        """Execute the modeling process and return a Pharmacophore."""
        pass
