import json
import os
from pathlib import Path
from typing import Any

from peek_tool.core.base import Inspector, InspectorFactory
from peek_tool.models.inspection_result import InspectionResult
from peek_tool.models.json_element import JsonElement, JsonRootElement


class JsonInspector(Inspector):
    """Inspector for JSON files and data structures."""

    def supports(self, target: str) -> bool:
        """Check if the target is a valid JSON file or a path to one."""
        # If the target is a file path, check if it exists and has a .json extension
        target_path = Path(target)
        if target_path.exists() and target_path.is_file():
            return target_path.suffix.lower() == ".json"

        # If the target contains path traversal notation for JSON (e.g., file.json:foo.bar)
        if ".json" in target and ":" in target:
            file_part = target.split(":")[0]
            return (
                Path(file_part).exists() and Path(file_part).suffix.lower() == ".json"
            )

        return False

    def inspect(self, target_name: str) -> InspectionResult:
        """Inspect a JSON file or a path within a JSON file."""
        # Handle path traversal if present (e.g., file.json:path.to.element)
        path_components = []
        if ":" in target_name:
            file_path, json_path = target_name.split(":", 1)
            path_components = json_path.split(".")
        else:
            file_path = target_name

        # Load the JSON file
        try:
            with open(file_path, "r") as f:
                json_data = json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to parse JSON file {file_path}: {str(e)}")

        # Create the root element
        file_name = os.path.basename(file_path)
        root_element = self._create_json_element(file_name, json_data)
        json_root = JsonRootElement(
            name=file_name, element=root_element, path=file_path
        )

        # If path components are specified, traverse to that element
        if path_components:
            try:
                current = json_data
                for component in path_components:
                    # Handle array indices
                    if component.isdigit() and isinstance(current, list):
                        index = int(component)
                        if 0 <= index < len(current):
                            current = current[index]
                        else:
                            raise ValueError(f"Array index {index} out of bounds")
                    # Handle object keys
                    elif isinstance(current, dict) and component in current:
                        current = current[component]
                    else:
                        raise ValueError(
                            f"Path component '{component}' not found in JSON"
                        )

                # Update the root element to point to the specified path
                path_element = self._create_json_element(
                    ".".join(path_components), current
                )
                json_root = JsonRootElement(
                    name=f"{file_name}:{'.'.join(path_components)}",
                    element=path_element,
                    path=file_path,
                )
            except Exception as e:
                raise ValueError(f"Failed to traverse JSON path: {str(e)}")

        # Create and return the inspection result
        return InspectionResult(
            name=json_root.name,
            type="json",
            elements=[json_root],
            metadata={"file_path": file_path},
        )

    def _create_json_element(self, name: str, data: Any) -> JsonElement:
        """Convert JSON data to a JsonElement."""
        if data is None:
            return JsonElement(name=name, value_type="null", value=None)

        if isinstance(data, dict):
            element = JsonElement(name=name, value_type="object")
            for key, value in data.items():
                element.children[key] = self._create_json_element(key, value)
            return element

        if isinstance(data, list):
            element = JsonElement(name=name, value_type="array")
            for i, item in enumerate(data):
                element.items.append(self._create_json_element(f"[{i}]", item))
            return element

        if isinstance(data, str):
            return JsonElement(name=name, value_type="string", value=data)

        if isinstance(data, (int, float)):
            return JsonElement(name=name, value_type="number", value=data)

        if isinstance(data, bool):
            return JsonElement(name=name, value_type="boolean", value=data)

        # For any other type, convert to string
        return JsonElement(name=name, value_type=type(data).__name__, value=str(data))


# Register the inspector
InspectorFactory.register("json", JsonInspector)
