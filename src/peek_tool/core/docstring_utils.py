"""Utilities for working with docstrings.

This module provides utilities for extracting, retrieving, paginating, and formatting docstrings
from Python modules, classes, methods, and functions.
"""

import inspect
import importlib
from typing import Dict, Any, Tuple, Optional

from peek_tool.formatters.docstring.text import DocstringTextFormatter


class DocstringExtractor:
    """Utility for extracting and paginating docstrings."""

    @classmethod
    def extract_docstring(cls, target: str) -> Tuple[str, str, Optional[str]]:
        """Extract docstring from a target.

        Args:
            target: The target to extract docstring from (e.g., 'json', 'json.dumps')

        Returns:
            A tuple containing:
            - The target type ('module', 'class', 'function', etc.)
            - The full docstring
            - The module name (or None if not applicable)

        Raises:
            ValueError: If the target cannot be found or has no docstring
        """
        # Try to import the target as a module first
        try:
            module = importlib.import_module(target)
            docstring = inspect.getdoc(module) or ""
            return "module", docstring, None
        except (ImportError, ModuleNotFoundError):
            # If that fails, try to handle it as a class, method, or function
            parts = target.split(".")

            # Handle module.attribute cases
            if len(parts) > 1:
                # First, try as a direct attribute of a module
                module_name = ".".join(parts[:-1])
                item_name = parts[-1]

                try:
                    module = importlib.import_module(module_name)
                    item = getattr(module, item_name)
                    docstring = inspect.getdoc(item) or ""

                    if inspect.isclass(item):
                        return "class", docstring, module_name
                    elif inspect.isfunction(item) or inspect.ismethod(item):
                        return "function", docstring, module_name
                    else:
                        return "attribute", docstring, module_name
                except (ImportError, AttributeError):
                    # If that fails, but we have at least 3 parts, check nested structures
                    if len(parts) > 2:
                        # Try handling as module.class.method or module.class.attribute
                        try:
                            class_module_name = ".".join(parts[:-2])
                            class_name = parts[-2]
                            method_name = parts[-1]

                            module = importlib.import_module(class_module_name)
                            class_obj = getattr(module, class_name)

                            if inspect.isclass(class_obj):
                                method = getattr(class_obj, method_name)
                                docstring = inspect.getdoc(method) or ""
                                return "function", docstring, class_module_name
                        except (ImportError, AttributeError):
                            # Multiple levels of module nesting possible
                            # Try each level of nesting to find a valid import path
                            for i in range(1, len(parts)):
                                try:
                                    module_prefix = ".".join(parts[:i])
                                    module = importlib.import_module(module_prefix)

                                    # Try to resolve the rest of the path
                                    current_obj = module
                                    for part in parts[i:]:
                                        current_obj = getattr(current_obj, part)

                                    docstring = inspect.getdoc(current_obj) or ""

                                    if inspect.isclass(current_obj):
                                        return "class", docstring, module_prefix
                                    elif inspect.isfunction(
                                        current_obj
                                    ) or inspect.ismethod(current_obj):
                                        return "function", docstring, module_prefix
                                    else:
                                        return "attribute", docstring, module_prefix
                                except (ImportError, AttributeError):
                                    continue

            # If all approaches fail
            raise ValueError(f"Could not find {target}")

    @classmethod
    def paginate_docstring(
        cls,
        docstring: str,
        page: int = 0,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Paginate a docstring.

        Args:
            docstring: The docstring to paginate
            page: The page number (0-indexed)
            page_size: Number of lines per page

        Returns:
            A dictionary with pagination information and content for the current page
        """
        if not docstring:
            return {
                "content": "(No docstring available)",
                "pagination": {
                    "page": 0,
                    "total_pages": 1,
                    "has_next": False,
                    "has_prev": False,
                },
            }

        # Split into lines for pagination
        lines = docstring.split("\n")
        total_lines = len(lines)
        total_pages = (total_lines + page_size - 1) // page_size

        # Validate page number
        if page >= total_pages:
            page = total_pages - 1
        if page < 0:
            page = 0

        # Calculate start and end indices
        start = page * page_size
        end = min(start + page_size, total_lines)

        # Get content for current page
        content = "\n".join(lines[start:end])

        # Return paginated content
        return {
            "content": content,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "total_lines": total_lines,
                "has_next": page < total_pages - 1,
                "has_prev": page > 0,
                "lines_range": f"{start + 1}-{end} of {total_lines}",
            },
        }

    @classmethod
    def format_docstring(cls, docstring: str) -> str:
        """Format a docstring to improve its readability.

        Args:
            docstring: The raw docstring to format

        Returns:
            A formatted docstring with improved readability
        """
        formatter = DocstringTextFormatter()
        return formatter.format(docstring)

    @classmethod
    def get_paginated_docstring(
        cls,
        target: str,
        page: int = 0,
        page_size: int = 20,
    ) -> Tuple[str, Dict[str, Any]]:
        """Get paginated docstring for a target.

        This combines extraction and pagination into a single operation.

        Args:
            target: The target to extract docstring from
            page: The page number (0-indexed)
            page_size: Number of lines per page

        Returns:
            A tuple containing:
            - A formatted string with the docstring content and pagination info
            - A dictionary with metadata (target, type, pagination info)
        """
        try:
            # Extract the docstring
            target_type, docstring, module_name = cls.extract_docstring(target)

            # Format the docstring to improve readability
            formatted_docstring = cls.format_docstring(docstring)

            # Paginate the formatted docstring
            result = cls.paginate_docstring(formatted_docstring, page, page_size)

            # Add target information
            result["target"] = target
            result["type"] = target_type
            if module_name:
                result["module"] = module_name

            # Extract content for rendering
            content = result.pop("content", "")

            # Create a formatted display string with pagination info
            rendered_text = cls._format_paginated_output(content, result)

            return rendered_text, result
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            metadata = {
                "error": str(e),
                "target": target,
                "pagination": {
                    "page": 0,
                    "total_pages": 1,
                    "has_next": False,
                    "has_prev": False,
                },
            }
            return error_msg, metadata

    @classmethod
    def _format_paginated_output(cls, content: str, metadata: Dict[str, Any]) -> str:
        """Format the paginated output with content and pagination information.

        Args:
            content: The docstring content
            metadata: Dictionary with pagination and target information

        Returns:
            A formatted string with content and pagination information
        """
        # Extract metadata
        pagination = metadata.get("pagination", {})
        target = metadata.get("target", "")
        target_type = metadata.get("type", "")
        module = metadata.get("module", "")

        # Build header
        header_parts = []
        if target:
            header_parts.append(f"Docstring for: {target}")
        if target_type:
            header_parts.append(f"Type: {target_type}")
        if module:
            header_parts.append(f"Module: {module}")

        header = " | ".join(header_parts)

        # Build pagination footer
        page = pagination.get("page", 0)
        total_pages = pagination.get("total_pages", 1)
        lines_range = pagination.get("lines_range", "")

        pagination_info = f"Page {page + 1}/{total_pages}"
        if lines_range:
            pagination_info += f" (Lines {lines_range})"

        # Add navigation hints if there are multiple pages
        nav_hints = []
        if pagination.get("has_prev", False):
            nav_hints.append("Use page={} for previous page".format(page))
        if pagination.get("has_next", False):
            nav_hints.append("Use page={} for next page".format(page + 2))

        # Combine everything
        result_parts = []

        # Add header if available
        if header:
            result_parts.append("─" * len(header))
            result_parts.append(header)
            result_parts.append("─" * len(header))
            result_parts.append("")  # Empty line after header

        # Add content
        result_parts.append(content)

        # Add footer if there's pagination
        if total_pages > 1:
            result_parts.append("")  # Empty line before footer
            result_parts.append("─" * len(pagination_info))
            result_parts.append(pagination_info)
            if nav_hints:
                result_parts.append(" | ".join(nav_hints))

        return "\n".join(result_parts)
