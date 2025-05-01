import argparse
import sys

from peek_tool.core.base import InspectorFactory
from peek_tool.formatters.base import FormatterFactory


def main():
    """Entry point for the peek CLI."""
    parser = argparse.ArgumentParser(
        description="Peek: Inspect Python modules and APIs"
    )

    parser.add_argument(
        "target", help="Target to inspect (e.g., a Python module or class)"
    )

    parser.add_argument(
        "--type",
        "-t",
        choices=["python"],  # Add more as implemented
        default="python",
        help="Type of target to inspect (default: python)",
    )

    parser.add_argument(
        "--format",
        "-f",
        choices=["text"],  # Add more as implemented
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    try:
        # Create the appropriate inspector
        inspector = InspectorFactory.create_inspector(args.type)

        # Check if the inspector supports the target
        if not inspector.supports(args.target):
            print(
                f"Error: Target '{args.target}' is not supported by the {args.type} inspector",
                file=sys.stderr,
            )
            sys.exit(1)

        # Perform the inspection
        result = inspector.inspect(args.target)

        # Format the results
        formatter = FormatterFactory.create_formatter(args.format)
        output = formatter.format(result)

        # Print the output
        print(output)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


# Entry point for the CLI
app = main


if __name__ == "__main__":
    main()
