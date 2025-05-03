"""Peek - Python module inspection and API discovery tool.

Peek is a tool for API discovery that helps you understand Python modules,
classes, and APIs through structured inspection and hierarchical navigation.
"""

__version__ = "0.1.0"

# Import key classes for easy access
from peek_tool.core.python_inspector import PythonInspector
from peek_tool.formatters.python.text import TextFormatter
from peek_tool.models.inspection_result import InspectionResult
from peek_tool.cli.app import app

__all__ = ["PythonInspector", "TextFormatter", "InspectionResult", "app"]
