"""Base docstring formatter.

This module provides the base class for docstring formatters.
"""

from abc import ABC, abstractmethod


class DocstringFormatter(ABC):
    """Base class for all docstring formatters."""

    @abstractmethod
    def format(self, docstring: str) -> str:
        """Format a docstring for display.

        Args:
            docstring: The raw docstring to format

        Returns:
            A formatted docstring
        """
        pass
