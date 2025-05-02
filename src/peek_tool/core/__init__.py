from peek_tool.core.base import Inspector, InspectorFactory
from peek_tool.core.python_inspector import PythonInspector
from peek_tool.core.json_inspector import JsonInspector

# Ensure inspectors are registered
__all__ = ["Inspector", "InspectorFactory", "PythonInspector", "JsonInspector"]
