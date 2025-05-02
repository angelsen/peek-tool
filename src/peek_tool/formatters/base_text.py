from abc import abstractmethod
from typing import List

from peek_tool.formatters.base import Formatter
from peek_tool.models.inspection_result import InspectionResult


class BaseTextFormatter(Formatter):
    """Base class for all text-based formatters.

    This class provides common text formatting functionality
    that can be shared across different text-based formatter types.
    """

    def format(self, result: InspectionResult) -> str:
        """Format inspection results as text.

        This base implementation handles the common header formatting
        and delegates specific element formatting to subclasses.
        """
        output = []

        # Format the header (common to all text formatters)
        self._format_header(result, output)

        # Format the content (implemented by subclasses)
        self._format_content(result, output)

        return "\n".join(output)

    def _format_header(self, result: InspectionResult, output: List[str]) -> None:
        """Format the header with name and type."""
        # Header with the name and type
        output.append(f"{result.name} ({result.type})")
        output.append("=" * len(output[0]))
        output.append("")

    @abstractmethod
    def _format_content(self, result: InspectionResult, output: List[str]) -> None:
        """Format the content of the inspection result.

        This abstract method must be implemented by subclasses to format
        the specific content based on the element types.
        """
        pass
