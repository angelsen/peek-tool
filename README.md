# Peek

A powerful Python module inspection and API discovery tool.

## Overview

Peek is a command-line tool and library for inspecting Python modules and their APIs. It extracts class and method information, type annotations, and docstrings to help developers understand Python libraries quickly and efficiently.

## Features

- **Complete Module Inspection**: Extract class, method, and function details from any installed Python module
- **Hierarchical Navigation**: Navigate from modules to classes to methods (e.g., `peek module.Class.method`)
- **Type Information**: Display parameter and return types from type annotations
- **Smart Import Handling**: Clearly identifies imported vs. locally defined items
- **Docstring Management**: Intelligently truncates docstrings for readability
- **Contextual Display**: Shows appropriate detail level based on current view
- **Multiple Output Formats**: Generate various output formats (currently text, more to come)
- **MCP Server Integration**: Expose peek functionality via the Model Context Protocol for LLM agents

## Installation

```bash
# Clone the repository
git clone https://github.com/angelsen/peek-tool.git
cd peek-tool

# Install the package
uv sync
```

## Basic Usage

### Command Line Interface

#### Inspect a Module

```bash
peek json
```

This shows the module's docstring, functions, classes, and imported items with a clean, hierarchical view.

#### Inspect a Specific Class

```bash
peek json.JSONEncoder
```

This shows the class's methods with their signatures (parameters and return types).

#### Inspect a Specific Method

```bash
peek json.JSONEncoder.encode
```

This shows detailed information about the method, including its full signature and docstring.

### MCP Server

Peek can also be run as an MCP (Model Context Protocol) server, exposing its functionality to LLM agents and other MCP clients.

#### Start the MCP server

```bash
peek-mcp
```

This starts an MCP server that exposes peek functionality as tools and resources that LLM agents can use.

#### Using with Claude and other MCP clients

The MCP server exposes:

1. `inspect_module` tool: Lets the LLM inspect any Python module
2. Help resources explaining how to use peek

To connect:
1. Start the peek-mcp server
2. Add it as a connection in Claude Desktop or any MCP client
3. The LLM can now use peek to inspect Python modules

## Project Structure

```
peek-tool/
├── src/
│   └── peek_tool/
│       ├── __init__.py        # Package exports
│       ├── core/              # Core inspection functionality
│       │   ├── base.py        # Abstract base classes
│       │   └── python_inspector.py # Python module inspection
│       ├── formatters/        # Output formatters
│       │   ├── base.py        # Formatter interface
│       │   └── text.py        # Text formatter
│       ├── models/            # Data models
│       │   ├── api_element.py # Models for API elements
│       │   └── inspection_result.py # Inspection results
│       ├── cli.py             # Command-line interface
│       └── mcp_server.py      # MCP server implementation
├── tests/                     # Test suite (coming soon)
└── README.md
```

## Development

### Prerequisites

- Python 3.11+
- UV for package management

### Setup

```bash
# Clone the repository
git clone https://github.com/angelsen/peek-tool.git
cd peek-tool

# Install development dependencies
uv sync
```

## Future Features

- Support for OpenAPI (Swagger) inspection
- Additional output formats (JSON, Markdown)
- Filtering options (e.g., `--no-private` to hide private methods)
- Depth control for adjusting verbosity level
- Interactive navigation mode
- Source code view with syntax highlighting
- Enhanced MCP integration with additional tools and resources
- Web UI for browsing inspection results

## Examples

### Inspecting Standard Library Modules

```bash
# View json module overview
peek json

# View details of the dumps function
peek json.dumps

# View the JSONEncoder class
peek json.JSONEncoder
```

### Inspecting Complex Third-Party Libraries

```bash
# Get an overview of a third-party package
peek requests

# View a specific submodule
peek requests.models

# Examine a specific class
peek requests.Session

# View details of a specific method
peek requests.Session.get
```

## License

MIT License