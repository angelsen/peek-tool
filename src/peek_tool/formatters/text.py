from typing import List

from peek_tool.formatters.base import Formatter, FormatterFactory
from peek_tool.models.inspection_result import InspectionResult
from peek_tool.models.api_element import Module, Class, Method, Parameter


class TextFormatter(Formatter):
    """Simple text formatter for inspection results."""

    def format(self, result: InspectionResult) -> str:
        """Format inspection results as plain text."""
        output = []

        # Header with the name and type
        output.append(f"{result.name} ({result.type})")
        output.append("=" * len(output[0]))
        output.append("")

        # Format each element
        for element in result.elements:
            if isinstance(element, Module):
                self._format_module(element, output)
            elif isinstance(element, Class):
                self._format_class(element, output, indent=0)
            elif isinstance(element, Method):
                self._format_method(element, output, indent=0)

        return "\n".join(output)

    def _format_module(self, module: Module, output: List[str]) -> None:
        """Format a module to text."""
        # Module docstring
        if module.docstring:
            output.append(f"Description: {module.docstring}")
            output.append("")

        # Module classes
        if module.classes:
            output.append("Classes:")
            output.append("-" * 7)
            for class_obj in module.classes:
                self._format_class(class_obj, output, indent=2)

        # Module functions
        if module.functions:
            output.append("Functions:")
            output.append("-" * 9)
            for function in module.functions:
                self._format_method(function, output, indent=2)

    def _format_class(self, class_obj: Class, output: List[str], indent: int) -> None:
        """Format a class to text."""
        indentation = " " * indent

        # Class name with base classes
        class_decl = f"{indentation}class {class_obj.name}"
        if class_obj.base_classes:
            base_classes_str = ", ".join(class_obj.base_classes)
            class_decl += f"({base_classes_str})"
        output.append(class_decl)

        # Class docstring
        if class_obj.docstring:
            output.append(f"{indentation}  Description: {class_obj.docstring}")

        # Class methods
        if class_obj.methods:
            output.append(f"{indentation}  Methods:")
            for method in class_obj.methods:
                self._format_method(method, output, indent=indent + 4)

        output.append("")  # Add an empty line after the class

    def _format_method(self, method: Method, output: List[str], indent: int) -> None:
        """Format a method or function to text."""
        indentation = " " * indent

        # Method signature with parameters
        params_str = ", ".join(
            self._format_parameter(param) for param in method.parameters
        )
        signature = f"{indentation}def {method.name}({params_str})"

        # Add return type if available
        if method.return_type:
            signature += f" -> {method.return_type}"

        output.append(signature)

        # Method docstring
        if method.docstring:
            output.append(f"{indentation}  Description: {method.docstring}")

        output.append("")  # Add an empty line after the method

    def _format_parameter(self, param: Parameter) -> str:
        """Format a parameter to a string for inclusion in a method signature."""
        result = param.name

        # Add type annotation if available
        if param.type_annotation:
            result += f": {param.type_annotation}"

        # Add default value if available
        if param.default_value:
            result += f" = {param.default_value}"

        return result


# Register the formatter
FormatterFactory.register("text", TextFormatter)
