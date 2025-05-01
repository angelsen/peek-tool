import inspect
import importlib
from typing import get_type_hints

from peek_tool.core.base import Inspector, InspectorFactory
from peek_tool.models.inspection_result import InspectionResult
from peek_tool.models.api_element import Module, Class, Method, Parameter


class PythonInspector(Inspector):
    """Inspector for Python modules and classes."""

    def supports(self, target: str) -> bool:
        """Check if the target is importable as a Python module."""
        try:
            # Try to import the module
            importlib.import_module(target)
            return True
        except (ImportError, ModuleNotFoundError):
            # Try to see if it's a class within a module
            parts = target.split(".")
            if len(parts) > 1:
                module_name = ".".join(parts[:-1])
                try:
                    importlib.import_module(module_name)
                    return True
                except (ImportError, ModuleNotFoundError):
                    pass
            return False

    def inspect(self, target_name: str) -> InspectionResult:
        """Inspect a Python module or class and return structured results."""
        # Try to import the target as a module first
        try:
            module = importlib.import_module(target_name)
            return self._inspect_module(module)
        except (ImportError, ModuleNotFoundError):
            # If that fails, try to find it as a class within a module
            parts = target_name.split(".")
            if len(parts) > 1:
                module_name = ".".join(parts[:-1])
                class_name = parts[-1]
                try:
                    module = importlib.import_module(module_name)
                    class_obj = getattr(module, class_name)
                    if inspect.isclass(class_obj):
                        return self._inspect_class_as_root(class_obj, target_name)
                except (ImportError, AttributeError):
                    pass

        raise ValueError(f"Could not import {target_name} as a Python module or class")

    def _inspect_module(self, module_obj) -> InspectionResult:
        """Inspect a Python module."""
        module_name = module_obj.__name__
        module_doc = inspect.getdoc(module_obj) or ""

        # Create a Module object
        module = Module(name=module_name, docstring=module_doc)

        # Find all classes in the module
        for name, obj in inspect.getmembers(module_obj, inspect.isclass):
            # Skip imported classes
            if obj.__module__ != module_name:
                continue

            class_info = self._inspect_class(obj)
            module.classes.append(class_info)

        # Find all functions in the module
        for name, obj in inspect.getmembers(module_obj, inspect.isfunction):
            # Skip imported functions
            if obj.__module__ != module_name:
                continue

            function_info = self._inspect_function(obj)
            module.functions.append(function_info)

        # Create and return the inspection result
        return InspectionResult(name=module_name, type="module", elements=[module])

    def _inspect_class_as_root(self, class_obj, full_name: str) -> InspectionResult:
        """Inspect a class as the root element."""
        class_info = self._inspect_class(class_obj)

        # Create and return the inspection result
        return InspectionResult(name=full_name, type="class", elements=[class_info])

    def _inspect_class(self, class_obj) -> Class:
        """Inspect a Python class."""
        class_name = class_obj.__name__
        class_doc = inspect.getdoc(class_obj) or ""
        base_classes = [
            base.__name__ for base in class_obj.__bases__ if base is not object
        ]

        # Create a Class object
        class_info = Class(
            name=class_name, docstring=class_doc, base_classes=base_classes
        )

        # Find all methods in the class
        for name, obj in inspect.getmembers(class_obj, inspect.isfunction):
            # Skip special methods (starting with __)
            if name.startswith("__") and name != "__init__":
                continue

            method_info = self._inspect_function(obj)
            class_info.methods.append(method_info)

        return class_info

    def _inspect_function(self, func_obj) -> Method:
        """Inspect a Python function or method."""
        func_name = func_obj.__name__
        func_doc = inspect.getdoc(func_obj) or ""

        # Get return type annotation if available
        return_type = None
        try:
            type_hints = get_type_hints(func_obj)
            if "return" in type_hints:
                return_type_obj = type_hints["return"]
                return_type = self._format_type_annotation(return_type_obj)
        except (TypeError, NameError):
            # Handle cases where type hints can't be resolved
            pass

        # Create a Method object
        method_info = Method(
            name=func_name, docstring=func_doc, return_type=return_type
        )

        # Get parameters
        signature = inspect.signature(func_obj)
        for param_name, param in signature.parameters.items():
            # Skip self parameter for methods
            if param_name == "self" and func_name != "__init__":
                continue

            # Get parameter type annotation if available
            param_type = None
            try:
                type_hints = get_type_hints(func_obj)
                if param_name in type_hints:
                    param_type_obj = type_hints[param_name]
                    param_type = self._format_type_annotation(param_type_obj)
            except (TypeError, NameError):
                # Handle cases where type hints can't be resolved
                pass

            # Get default value if available
            default_value = None
            if param.default is not param.empty:
                if param.default is None:
                    default_value = "None"
                elif isinstance(param.default, (str, int, float, bool)):
                    default_value = repr(param.default)
                else:
                    default_value = "..."  # For complex default values

            # Create a Parameter object
            param_info = Parameter(
                name=param_name, type_annotation=param_type, default_value=default_value
            )

            method_info.parameters.append(param_info)

        return method_info

    def _format_type_annotation(self, type_obj) -> str:
        """Format a type annotation as a string."""
        if type_obj is type(None):
            return "None"

        # Handle basic types
        if type_obj in (str, int, float, bool, list, dict, tuple, set):
            return type_obj.__name__

        # Handle typing module types
        type_str = str(type_obj)
        if type_str.startswith("typing."):
            return type_str.replace("typing.", "")

        return str(type_obj)


# Register the inspector
InspectorFactory.register("python", PythonInspector)
