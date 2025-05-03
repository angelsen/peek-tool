"""MCP server resources for peek-tool.

This module contains the resource definitions used by the peek MCP server.
"""

from peek_tool.mcp_server import server


@server.resource("mcp://peek/help")
def help_resource() -> str:
    """Documentation for using peek.

    Provides helpful information about how to use the peek tool
    and its capabilities for inspecting Python modules and JSON files.
    """
    return """# Peek-Tool

Peek is a tool for inspecting Python modules and JSON files.

## Inspect a Module

Use the `inspect_module` tool to inspect Python modules, classes, methods, or functions:

```python
inspect_module(target="json")  # Inspect the json module
inspect_module(target="json.JSONEncoder")  # Inspect a class
inspect_module(target="json.dumps")  # Inspect a function
inspect_module(target="json.JSONEncoder.encode")  # Inspect a method
```

## Inspect a JSON File

Use the `inspect_module` tool with a JSON file path:

```python
inspect_module(target="/path/to/file.json")  # Inspect a JSON file
inspect_module(target="/path/to/file.json:path.to.element")  # Inspect a specific element
```

## Parameters

- `target`: The Python module, class, function, method, or JSON file path to inspect

## Examples

Some examples of modules you can inspect:
- Standard library: `json`, `os`, `sys`, `datetime`
- Third-party modules (if installed): `requests`, `pandas`, `numpy`
- Local modules (if importable)
"""
