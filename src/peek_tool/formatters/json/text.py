from typing import List

from peek_tool.formatters.json.base import JsonFormatter
from peek_tool.formatters.base import FormatterFactory
from peek_tool.models.json_element import JsonElement, JsonRootElement


class JsonTextFormatter(JsonFormatter):
    """Plain text formatter for JSON inspection results."""

    def _format_json_root(self, root: JsonRootElement, output: List[str]) -> None:
        """Format a JSON root element."""
        # Add file path information
        output.append(f"File: {root.path}")
        output.append("")

        # Format the main element
        self._format_json_element(root.element, output, indent=0, depth=0)

    def _format_json_element(
        self, element: JsonElement, output: List[str], indent: int, depth: int
    ) -> None:
        """Format a JSON element to text."""
        indentation = " " * indent

        # Handle based on value type
        if element.value_type == "object":
            # For objects
            output.append(f"{indentation}{element.name}: {{")

            # Show object properties (key-value pairs)
            if depth < self.MAX_DISPLAY_DEPTH:
                for key, child in sorted(element.children.items()):
                    self._format_json_element(child, output, indent + 2, depth + 1)
            else:
                output.append(
                    f"{indentation}  ... (object with {len(element.children)} properties)"
                )

            output.append(f"{indentation}}}")

        elif element.value_type == "array":
            # For arrays
            output.append(f"{indentation}{element.name}: [")

            # Show array items (up to MAX_ARRAY_ITEMS)
            if depth < self.MAX_DISPLAY_DEPTH:
                items_to_show = min(len(element.items), self.MAX_ARRAY_ITEMS)
                for i in range(items_to_show):
                    self._format_json_element(
                        element.items[i], output, indent + 2, depth + 1
                    )

                # Show count if more items exist
                if len(element.items) > self.MAX_ARRAY_ITEMS:
                    output.append(
                        f"{indentation}  ... ({len(element.items) - self.MAX_ARRAY_ITEMS} more items)"
                    )
            else:
                output.append(
                    f"{indentation}  ... (array with {len(element.items)} items)"
                )

            output.append(f"{indentation}]")

        else:
            # For primitive values
            value_str = self._format_value(element.value, element.value_type)
            output.append(f"{indentation}{element.name}: {value_str}")


# Register the formatter
FormatterFactory.register("json-text", JsonTextFormatter)
