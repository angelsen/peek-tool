"""Inspect command group for the peek CLI."""

import typer
from peek_tool.cli.commands.inspect.command import inspect_command

app = typer.Typer(help="Inspect Python modules, classes, and JSON files")

# Register the command directly in the __init__ file
app.command()(inspect_command)

# Export the app for main.py to add
__all__ = ["app"]
