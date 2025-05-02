"""MCP server resources for peek-tool.

This module contains the resource definitions used by the peek MCP server.
"""

from mcp.server.fastmcp.server import FastMCP


def register_resources(app: FastMCP) -> None:
    """Register all peek resources with the FastMCP server."""

    @app.resource(
        uri="mcp://peek/help",
        name="Peek Help",
        description="Documentation for using peek",
    )
    def help_resource() -> str:
        """Return help documentation for peek."""
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

Use the `inspect_module` tool with a JSON file path and inspector_type="json":

```python
inspect_module(target="/path/to/file.json", inspector_type="json")  # Inspect a JSON file
inspect_module(target="/path/to/file.json:path.to.element", inspector_type="json")  # Inspect a specific element
```

## Parameters

- `target`: The Python module, class, function, method, or JSON file path to inspect
- `inspector_type`: Type of inspector to use ("python" or "json", default: "python")
- `output_format`: Output format ("text", "json-text", default: "text")

## Examples

Some examples of modules you can inspect:
- Standard library: `json`, `os`, `sys`, `datetime`
- Third-party modules (if installed): `requests`, `pandas`, `numpy`
- Local modules (if importable)
"""
