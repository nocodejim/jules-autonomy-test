import black
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any

def generate_python_sdk(schema: Dict[str, Any]) -> str:
    """
    Generates a Python SDK from a parsed OpenAPI schema.

    Args:
        schema: A dictionary representing the parsed OpenAPI schema.

    Returns:
        A string containing the generated Python SDK code.
    """
    env = Environment(loader=FileSystemLoader("templates/python"))
    template = env.get_template("sdk.py.j2")

    # This is a simplified representation of the data that will be passed to the template.
    # In a real implementation, this would be a more complex object with all the
    # necessary information extracted from the schema.
    template_data = {
        "class_name": "MyApiClient",
        "schema": schema,
    }

    raw_code = template.render(template_data)

    # Format the generated code using black
    try:
        formatted_code = black.format_str(raw_code, mode=black.FileMode())
    except black.InvalidInput:
        # If black fails to format the code, return the raw code
        # with a warning. This can happen if the generated code is
        # not valid Python.
        formatted_code = f"# WARNING: black formatting failed.\n\n{raw_code}"

    return formatted_code
