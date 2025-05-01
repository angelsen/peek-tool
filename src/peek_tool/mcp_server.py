"""MCP Server implementation for peek-tool.

This module provides an MCP server that exposes peek functionality
through the Model Context Protocol, allowing LLMs to inspect Python modules.
"""

import sys
from typing import Any, Dict, Optional

from mcp.server.fastmcp.server import FastMCP
from mcp.types import ImageContent, TextContent

from peek_tool.core.base import InspectorFactory
from peek_tool.formatters.base import FormatterFactory


def create_server(name: str = "Peek MCP Server",
                 instructions: str = "Inspect Python modules and their structure.") -> FastMCP:
    """Create and configure a FastMCP server for peek-tool."""
    app = FastMCP(name=name, instructions=instructions)

    @app.tool(
        name="inspect_module",
        description="Inspect a Python module, class, method or function and return its structure"
    )
    def inspect_module(
        target: str,
        inspector_type: str = "python",
        output_format: str = "text"
    ) -> str:
        """
        Inspect a Python module, class, method or function.

        Args:
            target: Target to inspect (e.g., a Python module or class name)
            inspector_type: Type of inspector to use (default: python)
            output_format: Output format (default: text)

        Returns:
            The formatted inspection result as text
        """
        try:
            # Create the appropriate inspector
            inspector = InspectorFactory.create_inspector(inspector_type)

            # Check if the inspector supports the target
            if not inspector.supports(target):
                return f"Error: Target '{target}' is not supported by the {inspector_type} inspector"

            # Perform the inspection
            result = inspector.inspect(target)

            # Format the results
            formatter = FormatterFactory.create_formatter(output_format)
            output = formatter.format(result)

            return output

        except Exception as e:
            return f"Error: {str(e)}"

    @app.resource(
        uri="mcp://peek/help",
        name="Peek Help",
        description="Documentation for using peek"
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

    return app


def main():
    """Run the MCP server."""
    app = create_server()
    app.run()


if __name__ == "__main__":
    main()