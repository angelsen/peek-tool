# Setting Up a FastMCP Server

This guide explains how to set up a FastMCP server based on the Model Context Protocol (MCP) using the `mcp` Python package. FastMCP provides a high-level, ergonomic interface for creating MCP servers that can expose data and functionality to LLMs.

## Prerequisites

Before setting up your FastMCP server, ensure you have the following:

1. Python 3.11 or higher
2. The `mcp` package installed: `uv pip install mcp`

## Understanding MCP

MCP (Model Context Protocol) is an open protocol that standardizes how applications provide context to LLMs. It follows a client-server architecture where:

- **MCP Clients**: Applications like Claude Desktop or IDEs that want to access data through MCP
- **MCP Servers**: Programs that expose specific capabilities (resources, tools, prompts) through the standardized protocol

## Steps to Create a FastMCP Server

### 1. Install Required Dependencies

```bash
uv pip install mcp anyio httpx pydantic starlette uvicorn
```

### 2. Create a Basic FastMCP Server

Here's a minimal example of a FastMCP server:

```python
from mcp.server.fastmcp.server import FastMCP

# Create a FastMCP server instance
app = FastMCP(
    name="My MCP Server",
    instructions="This server provides custom tools and resources."
)

# Define a simple tool
@app.tool(name="greeting", description="Returns a greeting message")
def greeting(name: str) -> str:
    """Return a greeting message for the given name."""
    return f"Hello, {name}!"

# Run the server (stdio is the default transport)
if __name__ == "__main__":
    app.run()
```

### 3. Adding Resources

Resources allow your server to expose data to LLMs:

```python
# Add a function-based resource
@app.resource(
    uri="mcp://myserver/example",
    name="Example Resource",
    description="An example resource"
)
def example_resource():
    return "This is an example resource content."

# You can also add file-based resources
from mcp.server.fastmcp.resources.types import FileResource

file_resource = FileResource(
    uri="mcp://myserver/file",
    name="File Resource",
    description="A file-based resource",
    path="/path/to/your/file.txt"
)
app.add_resource(file_resource)
```

### 4. Adding Prompts

Prompts are templates that can be used by LLMs:

```python
from mcp.server.fastmcp.prompts.base import Prompt

# Define a prompt template
prompt = Prompt(
    name="greeting_prompt",
    description="A template for generating a greeting",
    template="Hello, {name}! Welcome to {place}.",
    arguments={
        "name": {"type": "string", "description": "The name to greet"},
        "place": {"type": "string", "description": "The place name"}
    }
)
app.add_prompt(prompt)
```

### 5. Transport Options

FastMCP supports different transport mechanisms:

```python
# Run with stdio (default)
app.run(transport="stdio")

# Run with SSE (Server-Sent Events)
app.run(transport="sse")

# For more control over SSE setup
async def run_sse():
    await app.run_sse_async()
```

### 6. Complete Example

Here's a more complete example with resources, tools, and prompts:

```python
from mcp.server.fastmcp.server import FastMCP
from mcp.server.fastmcp.prompts.base import Prompt
from mcp.server.fastmcp.resources.types import TextResource

app = FastMCP(
    name="Demo MCP Server",
    instructions="This server demonstrates MCP capabilities."
)

# Add tools
@app.tool(name="calculator", description="Performs basic calculations")
def calculator(operation: str, a: float, b: float) -> str:
    """Perform basic calculations."""
    if operation == "add":
        return f"{a} + {b} = {a + b}"
    elif operation == "subtract":
        return f"{a} - {b} = {a - b}"
    elif operation == "multiply":
        return f"{a} * {b} = {a * b}"
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero"
        return f"{a} / {b} = {a / b}"
    else:
        return f"Unknown operation: {operation}"

# Add resources
@app.resource(
    uri="mcp://demo/help",
    name="Help Documentation",
    description="Documentation about using this server"
)
def help_doc():
    return """
    # Demo MCP Server
    
    This server provides calculation tools and documentation.
    
    Available tools:
    - calculator: Performs basic math operations
    
    Example usage:
    calculator(operation="add", a=5, b=3)
    """

# Add a prompt
prompt = Prompt(
    name="math_problem",
    description="A template for describing a math problem",
    template="I need to {operation} the numbers {a} and {b}. What is the result?",
    arguments={
        "operation": {"type": "string", "description": "The math operation"},
        "a": {"type": "number", "description": "First number"},
        "b": {"type": "number", "description": "Second number"}
    }
)
app.add_prompt(prompt)

if __name__ == "__main__":
    app.run()
```

## Client Connection

MCP clients, like Claude Desktop or custom applications, can connect to your server to access the resources, tools, and prompts you've defined.

### Using with Claude Desktop

1. Start your FastMCP server
2. Open Claude Desktop
3. Add your MCP server in Claude Desktop settings
4. Claude can now use your server's capabilities

## Security Considerations

- MCP servers should follow the principle of least privilege
- Consider what data and functionality you expose
- For production use, implement proper authentication and authorization

## Debugging

During development, you can use the MCP Inspector tool for debugging:
- Visit: https://modelcontextprotocol.io/docs/tools/inspector
- Connect to your running MCP server
- Inspect available resources, tools, and prompts

## Next Steps

- Implement more complex tools and resources
- Explore additional FastMCP capabilities
- Consider using SSE transport for web applications
- Add proper error handling and logging

This guide provides the basics for setting up a FastMCP server. For more advanced usage, refer to the official MCP documentation.