from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class JsonElement:
    """Represents a JSON element or structure."""

    name: str
    value_type: str  # 'object', 'array', 'string', 'number', 'boolean', 'null'

    # For objects and arrays
    children: Dict[str, "JsonElement"] = field(default_factory=dict)
    items: List["JsonElement"] = field(default_factory=list)

    # For primitive values
    value: Optional[Any] = None

    # For all elements
    description: Optional[str] = None
    schema_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JsonRootElement:
    """Represents the root of a JSON document."""

    name: str  # Usually the filename or path
    element: JsonElement
    path: str  # Original file path

    # Additional metadata about the JSON document
    metadata: Dict[str, Any] = field(default_factory=dict)
