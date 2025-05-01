from abc import ABC, abstractmethod
from typing import Dict, Type

from peek_tool.models.inspection_result import InspectionResult


class Inspector(ABC):
    """Base class for all inspectors."""

    @abstractmethod
    def inspect(self, target_name: str) -> InspectionResult:
        """Inspect a target and return structured results."""
        pass

    @abstractmethod
    def supports(self, target: str) -> bool:
        """Check if this inspector supports the given target."""
        pass


class InspectorFactory:
    """Factory for creating appropriate inspectors based on target type."""

    _inspectors: Dict[str, Type[Inspector]] = {}

    @classmethod
    def register(cls, name: str, inspector_class: Type[Inspector]):
        """Register an inspector class for a specific target type."""
        cls._inspectors[name] = inspector_class

    @classmethod
    def create_inspector(cls, target_type: str) -> Inspector:
        """Create and return appropriate inspector for the target type."""
        if target_type not in cls._inspectors:
            raise ValueError(f"No inspector registered for target type: {target_type}")

        return cls._inspectors[target_type]()
