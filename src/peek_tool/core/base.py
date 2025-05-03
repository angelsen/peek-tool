from abc import ABC, abstractmethod
from pathlib import Path
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

    # Map inspector types to their formatter types
    _formatter_mappings: Dict[str, str] = {
        "python": "text",
        "json": "json-text",
        # Add more mappings as needed
    }

    @classmethod
    def register(
        cls, name: str, inspector_class: Type[Inspector], formatter_type: str = None
    ):
        """Register an inspector class with its associated formatter."""
        cls._inspectors[name] = inspector_class
        if formatter_type:
            cls._formatter_mappings[name] = formatter_type

    @classmethod
    def create_inspector(cls, target_type: str) -> Inspector:
        """Create and return appropriate inspector for the target type."""
        if target_type not in cls._inspectors:
            raise ValueError(f"No inspector registered for target type: {target_type}")

        return cls._inspectors[target_type]()

    @classmethod
    def detect_inspector_type(cls, target: str) -> str:
        """Auto-detect the type of target based on its characteristics."""
        # Check if it's a file path with extension
        path = Path(target.split(":")[0] if ":" in target else target)
        if path.exists() and path.is_file():
            extension = path.suffix.lower()
            if extension == ".json":
                return "json"
            # Add more file types as needed

        # Default to Python for other targets
        return "python"

    @classmethod
    def get_formatter_for_inspector(cls, inspector_type: str) -> str:
        """Get the formatter type associated with an inspector type."""
        return cls._formatter_mappings.get(inspector_type, "text")

    @classmethod
    def inspect(cls, target: str) -> str:
        """
        Perform a complete inspection operation with automatic type detection
        and formatter selection.

        Args:
            target: The target to inspect

        Returns:
            Formatted inspection result as a string

        Raises:
            ValueError: If inspection fails
        """
        # Auto-detect inspector type
        detected_type = cls.detect_inspector_type(target)

        # Create the appropriate inspector
        inspector = cls.create_inspector(detected_type)

        # Validate that the inspector supports this target
        if not inspector.supports(target):
            raise ValueError(
                f"Target '{target}' is not supported by the {detected_type} inspector"
            )

        # Perform the inspection
        result = inspector.inspect(target)

        # Get the associated formatter
        format_type = cls.get_formatter_for_inspector(detected_type)

        # Create and use the formatter
        from peek_tool.formatters.base import FormatterFactory

        formatter = FormatterFactory.create_formatter(format_type)
        output = formatter.format(result)

        return output
