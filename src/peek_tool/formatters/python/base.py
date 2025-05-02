from abc import abstractmethod
from typing import List

from peek_tool.formatters.base_text import BaseTextFormatter
from peek_tool.models.python_element import Module, Class, Method, Parameter
from peek_tool.models.inspection_result import InspectionResult


class PythonFormatter(BaseTextFormatter):
    """Base class for Python-specific formatters.

    This class provides common functionality for formatting Python
    inspection results, including modules, classes, and methods.
    """

    # Default truncation limits for docstrings
    MAX_DOCSTRING_LINES = 8
    MAX_FUNCTION_DOCSTRING_LINES = 15

    def _format_content(self, result: InspectionResult, output: List[str]) -> None:
        """Format Python inspection result elements."""
        for element in result.elements:
            if isinstance(element, Module):
                self._format_module(element, output)
            elif isinstance(element, Class):
                self._format_class(element, output, indent=0)
            elif isinstance(element, Method):
                self._format_method(element, output, indent=0)

    def _truncate_docstring(self, docstring: str, max_lines: int) -> str:
        """Truncate a docstring to a maximum number of lines."""
        if not docstring:
            return ""

        lines = docstring.split("\n")
        if len(lines) <= max_lines:
            return docstring

        truncated = "\n".join(lines[:max_lines])
        return f"{truncated}\n\n[...docstring truncated...]"

    @abstractmethod
    def _format_module(self, module: Module, output: List[str]) -> None:
        """Format a module to text."""
        pass

    @abstractmethod
    def _format_class(self, class_obj: Class, output: List[str], indent: int) -> None:
        """Format a class to text."""
        pass

    @abstractmethod
    def _format_method(self, method: Method, output: List[str], indent: int) -> None:
        """Format a method or function to text."""
        pass

    def _format_parameter(self, param: Parameter) -> str:
        """Format a parameter to a string for inclusion in a method signature."""
        result = param.name

        # Add type annotation if available
        if param.type_annotation:
            result += f": {param.type_annotation}"

        # Add default value if available
        if param.default_value:
            result += f" = {param.default_value}"

        return result
