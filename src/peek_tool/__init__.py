"""
Peek: A powerful Python module inspection and API discovery tool.
"""

__version__ = "0.1.0"

# Import key classes for easy access
from peek_tool.core.python_inspector import PythonInspector
from peek_tool.formatters.python.text import TextFormatter
from peek_tool.models.inspection_result import InspectionResult

__all__ = ["PythonInspector", "TextFormatter", "InspectionResult"]
