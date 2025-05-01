from dataclasses import dataclass, field
from typing import List, Dict, Any, Union
from peek_tool.models.api_element import Module, Class, Method


@dataclass
class InspectionResult:
    """Container for inspection results."""

    name: str
    type: str  # 'module', 'class', 'openapi', etc.
    elements: List[Union[Module, Class, Method]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
