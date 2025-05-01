from typing import List

from peek_tool.formatters.base import Formatter, FormatterFactory
from peek_tool.models.inspection_result import InspectionResult
from peek_tool.models.api_element import Module, Class, Method, Parameter


class TextFormatter(Formatter):
    """Simple text formatter for inspection results."""
    
    # Max number of lines to show for docstrings at top level
    MAX_DOCSTRING_LINES = 8
    
    # Max number of lines to show for function/method details
    MAX_FUNCTION_DOCSTRING_LINES = 15

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
    
    def _truncate_docstring(self, docstring: str, max_lines: int) -> str:
        """Truncate a docstring to a maximum number of lines."""
        if not docstring:
            return ""
            
        lines = docstring.split('\n')
        if len(lines) <= max_lines:
            return docstring
            
        truncated = '\n'.join(lines[:max_lines])
        return f"{truncated}\n\n[...docstring truncated...]"

    def _format_module(self, module: Module, output: List[str]) -> None:
        """Format a module to text."""
        # Module docstring (truncated)
        if module.docstring:
            truncated_doc = self._truncate_docstring(module.docstring, self.MAX_DOCSTRING_LINES)
            output.append(f"Description: {truncated_doc}")
            output.append("")
            
        # Show submodules if present
        if module.submodules:
            output.append("Submodules:")
            for submodule in module.submodules:
                output.append(f"  {submodule}")
            output.append("")

        # Get directly defined classes (not imported)
        local_classes = [c for c in module.classes if not c.is_imported]
        if local_classes:
            output.append("Classes:")
            output.append("-" * 7)
            for class_obj in local_classes:
                # Simplified class listing at module level
                indentation = " " * 2
                class_decl = f"{indentation}class {class_obj.name}"
                if class_obj.base_classes:
                    base_classes_str = ", ".join(class_obj.base_classes)
                    class_decl += f"({base_classes_str})"
                output.append(class_decl)
            output.append("")

        # Get directly defined functions (not imported)
        local_functions = [f for f in module.functions if not f.is_imported]
        if local_functions:
            output.append("Functions:")
            output.append("-" * 9)
            for function in local_functions:
                # Simplified function listing at module level
                indentation = " " * 2
                params_str = ", ".join(
                    self._format_parameter(param) for param in function.parameters
                )
                signature = f"{indentation}def {function.name}({params_str})"
                if function.return_type:
                    signature += f" -> {function.return_type}"
                output.append(signature)
            output.append("")
            
        # Group imported classes by source module
        imported_classes = {}
        for class_obj in module.classes:
            if class_obj.is_imported and class_obj.import_source:
                source = class_obj.import_source
                if source not in imported_classes:
                    imported_classes[source] = []
                imported_classes[source].append(class_obj.name)
                
        # Group imported functions by source module
        imported_functions = {}
        for function in module.functions:
            if function.is_imported and function.import_source:
                source = function.import_source
                if source not in imported_functions:
                    imported_functions[source] = []
                imported_functions[source].append(function.name)
        
        # Show imported classes
        if imported_classes:
            output.append("Imported Classes:")
            for source, names in sorted(imported_classes.items()):
                output.append(f"  From {source}:")
                output.append("    " + ", ".join(sorted(names)))
            output.append("")
            
        # Show imported functions
        if imported_functions:
            output.append("Imported Functions:")
            for source, names in sorted(imported_functions.items()):
                output.append(f"  From {source}:")
                output.append("    " + ", ".join(sorted(names)))
            output.append("")

    def _format_class(self, class_obj: Class, output: List[str], indent: int) -> None:
        """Format a class to text."""
        indentation = " " * indent

        # Class name with base classes
        class_decl = f"{indentation}class {class_obj.name}"
        if class_obj.base_classes:
            base_classes_str = ", ".join(class_obj.base_classes)
            class_decl += f"({base_classes_str})"
        
        # Add import information if relevant
        if class_obj.is_imported and class_obj.import_source:
            class_decl += f" [imported from {class_obj.import_source}]"
            
        output.append(class_decl)

        # Class docstring (truncated if at module level)
        if class_obj.docstring:
            # If showing class directly (indent=0), show more of the docstring
            max_lines = self.MAX_FUNCTION_DOCSTRING_LINES if indent == 0 else self.MAX_DOCSTRING_LINES
            truncated_doc = self._truncate_docstring(class_obj.docstring, max_lines)
            output.append(f"{indentation}  Description: {truncated_doc}")

        # Class methods
        if class_obj.methods:
            output.append(f"{indentation}  Methods:")
            for method in class_obj.methods:
                method_indentation = " " * (indent + 4)
                
                # Format method signature with parameters
                params_str = ", ".join(
                    self._format_parameter(param) for param in method.parameters
                )
                method_sig = f"def {method.name}({params_str})"
                
                # Add return type if available
                if method.return_type:
                    method_sig += f" -> {method.return_type}"
                    
                # Add import information if relevant
                if method.is_imported and method.import_source:
                    method_sig += f" [imported from {method.import_source}]"
                    
                output.append(f"{method_indentation}{method_sig}")

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
            
        # Add import information if relevant
        if method.is_imported and method.import_source:
            signature += f" [imported from {method.import_source}]"

        output.append(signature)

        # Only show docstring when looking directly at a function (indent=0)
        # This means methods in classes won't show docstrings by default
        if method.docstring and indent == 0:
            max_lines = self.MAX_FUNCTION_DOCSTRING_LINES
            truncated_doc = self._truncate_docstring(method.docstring, max_lines)
            output.append(f"{indentation}  Description: {truncated_doc}")

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
