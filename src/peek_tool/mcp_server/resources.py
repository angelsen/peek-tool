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

Peek is a tool for inspecting Python modules and their structure.

## Inspect a Module

Use the `inspect_module` tool to inspect Python modules, classes, methods, or functions:

```python
inspect_module(target="json")  # Inspect the json module
inspect_module(target="json.JSONEncoder")  # Inspect a class
inspect_module(target="json.dumps")  # Inspect a function
inspect_module(target="json.JSONEncoder.encode")  # Inspect a method
```

## Parameters

- `target`: The Python module, class, function, or method to inspect
- `inspector_type`: Type of inspector to use (default: "python")
- `output_format`: Output format (default: "text")

## Examples

Some examples of modules you can inspect:
- Standard library: `json`, `os`, `sys`, `datetime`
- Third-party modules (if installed): `requests`, `pandas`, `numpy`
- Local modules (if importable)
"""
