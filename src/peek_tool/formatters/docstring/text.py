"""Text formatter for docstrings.

This module provides a text-based formatter for docstrings, improving
their readability by normalizing indentation, highlighting sections,
and formatting code examples.
"""

from typing import List

from peek_tool.formatters.docstring.base import DocstringFormatter


class DocstringTextFormatter(DocstringFormatter):
    """Text formatter for docstrings.

    This formatter improves the readability of docstrings by:
    - Normalizing indentation
    - Highlighting section headers (Args, Returns, etc.)
    - Improving the formatting of code examples
    - Aligning parameter descriptions
    """

    # Common section headers in docstrings
    SECTION_HEADERS = [
        "Args:",
        "Arguments:",
        "Parameters:",
        "Returns:",
        "Return:",
        "Yields:",
        "Raises:",
        "Exceptions:",
        "Example:",
        "Examples:",
        "Note:",
        "Notes:",
        "Warning:",
        "Warnings:",
    ]

    def format(self, docstring: str) -> str:
        """Format a docstring for improved readability.

        Args:
            docstring: The raw docstring to format

        Returns:
            A formatted docstring with normalized indentation and improved
            section formatting.
        """
        if not docstring:
            return "(No docstring available)"

        # Normalize line endings
        docstring = docstring.replace("\r\n", "\n")

        # Split into lines for processing
        lines = docstring.split("\n")

        # Format the docstring
        formatted_lines = self._process_lines(lines)

        # Join lines back together
        return "\n".join(formatted_lines)

    def _process_lines(self, lines: List[str]) -> List[str]:
        """Process docstring lines for formatting.

        Args:
            lines: The docstring split into lines

        Returns:
            A list of processed lines with improved formatting
        """
        # Normalize indentation first
        lines = self._normalize_indentation(lines)

        # Format sections
        formatted_lines = []
        in_code_block = False
        current_section = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Handle code block detection
            if stripped.startswith("```") or stripped.startswith(":::"):
                in_code_block = not in_code_block
                formatted_lines.append(line)
                continue

            # Don't format content inside code blocks
            if in_code_block:
                formatted_lines.append(line)
                continue

            # Check for section headers
            is_section_header = False
            for header in self.SECTION_HEADERS:
                if stripped == header or stripped.startswith(f"{header} "):
                    current_section = header.rstrip(":")
                    is_section_header = True
                    # Add extra spacing before sections (except the first line)
                    if i > 0 and formatted_lines and formatted_lines[-1].strip():
                        formatted_lines.append("")
                    formatted_lines.append(line)
                    break

            if is_section_header:
                continue

            # Handle parameter descriptions in Args sections
            if (
                current_section in ["Args", "Arguments", "Parameters"]
                and stripped
                and ":" in stripped
            ):
                # This is likely a parameter description
                param_parts = stripped.split(":", 1)
                if len(param_parts) == 2 and not param_parts[0].strip().startswith(
                    "- "
                ):
                    param_name = param_parts[0].strip()
                    param_desc = param_parts[1].strip()
                    formatted_lines.append(f"    {param_name}: {param_desc}")
                    continue

            # Add normal line
            formatted_lines.append(line)

        return formatted_lines

    def _normalize_indentation(self, lines: List[str]) -> List[str]:
        """Normalize the indentation in a docstring.

        Args:
            lines: The docstring split into lines

        Returns:
            Lines with normalized indentation
        """
        # Find the minimum indentation of non-empty lines
        indentation_levels = []
        for line in lines:
            if line.strip():  # Skip empty lines
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                indentation_levels.append(indent)

        # If no non-empty lines, return original
        if not indentation_levels:
            return lines

        # Calculate common indentation to remove
        min_indent = min(indentation_levels)

        # Remove the common indentation from all lines
        normalized_lines = []
        for line in lines:
            if line.strip():  # Only process non-empty lines
                normalized_lines.append(line[min_indent:])
            else:
                normalized_lines.append("")  # Keep empty lines as empty

        return normalized_lines
