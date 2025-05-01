# Peek

A powerful Python module inspection and API discovery tool.

## Overview

Peek is a command-line tool and library for inspecting Python modules and their APIs. It extracts class and method information, type annotations, and docstrings to help developers understand Python libraries quickly.

## Features

- **Module Inspection**: Extract class and method details from any installed Python module
- **Type Information**: Display parameter and return types from type annotations
- **Multiple Output Formats**: Generate various output formats (currently text, more to come)

## Installation

```bash
# Clone the repository
git clone https://github.com/angelsen/peek-tool.git
cd peek-tool

# Install the package
uv sync
```

## Basic Usage

### Inspect a Module

```bash
peek json
```

### Inspect a Specific Class

```bash
peek json.JSONEncoder
```

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
│       └── cli.py             # Command-line interface
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
- Extended type support

## License

MIT License