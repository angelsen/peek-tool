from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Parameter:
    """Represents a parameter in a method or function."""

    name: str
    type_annotation: Optional[str] = None
    default_value: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Method:
    """Represents a method or function."""

    name: str
    parameters: List[Parameter] = field(default_factory=list)
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    decorators: List[str] = field(default_factory=list)


@dataclass
class Class:
    """Represents a class."""

    name: str
    methods: List[Method] = field(default_factory=list)
    base_classes: List[str] = field(default_factory=list)
    docstring: Optional[str] = None


@dataclass
class Module:
    """Represents a Python module."""

    name: str
    classes: List[Class] = field(default_factory=list)
    functions: List[Method] = field(default_factory=list)
    docstring: Optional[str] = None
