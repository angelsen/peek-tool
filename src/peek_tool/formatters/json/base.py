from abc import abstractmethod
from typing import List, Any

from peek_tool.formatters.base_text import BaseTextFormatter
from peek_tool.models.inspection_result import InspectionResult
from peek_tool.models.json_element import JsonElement, JsonRootElement


class JsonFormatter(BaseTextFormatter):
    """Base class for JSON-specific formatters.

    This class provides common functionality for formatting JSON
    inspection results, including objects, arrays, and primitive values.
    """

    # Default display configuration
    MAX_ARRAY_ITEMS = 10
    MAX_DISPLAY_DEPTH = 1
    MAX_STRING_LENGTH = 80

    def _format_content(self, result: InspectionResult, output: List[str]) -> None:
        """Format JSON inspection result elements."""
        for element in result.elements:
            if isinstance(element, JsonRootElement):
                self._format_json_root(element, output)

    @abstractmethod
    def _format_json_root(self, root: JsonRootElement, output: List[str]) -> None:
        """Format a JSON root element."""
        pass

    @abstractmethod
    def _format_json_element(
        self, element: JsonElement, output: List[str], indent: int, depth: int
    ) -> None:
        """Format a JSON element to text."""
        pass

    def _format_value(self, value: Any, value_type: str) -> str:
        """Format a JSON value based on its type."""
        if value is None:
            return "null"

        if value_type == "string":
            # Truncate long strings
            if len(value) > self.MAX_STRING_LENGTH:
                return f'"{value[: self.MAX_STRING_LENGTH]}..." (truncated)'
            return f'"{value}"'

        if value_type == "number":
            return str(value)

        if value_type == "boolean":
            return str(value).lower()

        # For any other type
        return str(value)
