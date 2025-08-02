from prance import ResolvingParser

def parse_openapi(url: str):
    """
    Parses an OpenAPI/Swagger documentation from a URL.

    Args:
        url: The URL of the OpenAPI/Swagger documentation.

    Returns:
        A dictionary representing the parsed OpenAPI/Swagger documentation.
    """
    parser = ResolvingParser(url)
    return parser.specification
