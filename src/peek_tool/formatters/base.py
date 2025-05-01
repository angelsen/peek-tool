from abc import ABC, abstractmethod
from typing import Dict, Type

from peek_tool.models.inspection_result import InspectionResult


class Formatter(ABC):
    """Base class for all output formatters."""

    @abstractmethod
    def format(self, result: InspectionResult) -> str:
        """Format inspection results into a string."""
        pass


class FormatterFactory:
    """Factory for creating appropriate formatters based on format type."""

    _formatters: Dict[str, Type[Formatter]] = {}

    @classmethod
    def register(cls, name: str, formatter_class: Type[Formatter]):
        """Register a formatter class for a specific format type."""
        cls._formatters[name] = formatter_class

    @classmethod
    def create_formatter(cls, format_type: str) -> Formatter:
        """Create and return appropriate formatter for the output format."""
        if format_type not in cls._formatters:
            raise ValueError(f"No formatter registered for format type: {format_type}")

        return cls._formatters[format_type]()
