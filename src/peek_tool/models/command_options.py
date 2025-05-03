"""Command option dataclasses for the peek CLI."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class InspectOptions:
    """Options for the inspect command."""

    target: str


@dataclass(frozen=True)
class McpServerOptions:
    """Options for the MCP server command."""

    name: str = "Peek"
    transport: str = "stdio"


@dataclass(frozen=True)
class McpInitOptions:
    """Options for the MCP init command."""

    target: Optional[str] = None
    scope: Optional[str] = None
    name: Optional[str] = None
    package_manager: Optional[str] = None
    interactive: bool = True
