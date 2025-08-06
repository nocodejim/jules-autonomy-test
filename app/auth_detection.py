from typing import Dict, Any, List

def detect_auth(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes a parsed OpenAPI schema to identify the authentication methods used.

    Args:
        schema: A dictionary representing the parsed OpenAPI schema.

    Returns:
        A dictionary summarizing the detected authentication methods.
    """
    if not isinstance(schema, dict):
        return {"error": "Invalid schema format: not a dictionary"}

    security_schemes = schema.get("components", {}).get("securitySchemes", {})
    if not security_schemes:
        return {"authentication": "No security schemes found."}

    detected_methods = []

    for name, details in security_schemes.items():
        auth_type = details.get("type")
        method_summary = {"name": name, "type": auth_type}

        if auth_type == "apiKey":
            method_summary["in"] = details.get("in")
            method_summary["param_name"] = details.get("name")
        elif auth_type == "http":
            scheme = details.get("scheme", "").lower()
            method_summary["scheme"] = scheme
            if scheme == "bearer":
                method_summary["description"] = "Typically a JWT or an opaque token."
        elif auth_type == "oauth2":
            method_summary["flows"] = {}
            for flow_name, flow_details in details.get("flows", {}).items():
                method_summary["flows"][flow_name] = {
                    "authorizationUrl": flow_details.get("authorizationUrl"),
                    "tokenUrl": flow_details.get("tokenUrl"),
                    "scopes": list(flow_details.get("scopes", {}).keys()),
                }

        detected_methods.append(method_summary)

    # Check the top-level security field to see which schemes are actively used
    active_security = schema.get("security", [])
    active_schemes = [list(req.keys())[0] for req in active_security if req]

    return {
        "detected_schemes": detected_methods,
        "active_schemes": active_schemes
    }
