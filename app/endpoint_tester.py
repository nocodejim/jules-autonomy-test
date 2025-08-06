import httpx
import asyncio
from typing import Dict, Any, List

async def test_single_endpoint(client: httpx.AsyncClient, base_url: str, path: str, method: str) -> Dict[str, Any]:
    """
    Tests a single endpoint with a given HTTP method.
    """
    url = f"{base_url.rstrip('/')}{path}"
    try:
        response = await client.request(method, url, timeout=10.0)
        return {
            "method": method,
            "url": url,
            "status_code": response.status_code,
            "reason": response.reason_phrase
        }
    except httpx.RequestError as e:
        return {
            "method": method,
            "url": url,
            "status_code": None,
            "error": f"Request failed: {type(e).__name__}"
        }

async def test_endpoints(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Performs a basic liveness test on endpoints listed in an OpenAPI schema.

    Args:
        schema: A dictionary representing the parsed OpenAPI schema.

    Returns:
        A list of dictionaries summarizing the test results for each endpoint.
    """
    servers = schema.get("servers", [{"url": "/"}])
    if not servers:
        return [{"error": "No servers found in the schema."}]

    # For simplicity, we'll use the first server URL.
    # A more robust implementation might test against all specified servers.
    base_url = servers[0].get("url", "/")

    paths = schema.get("paths", {})
    if not paths:
        return [{"error": "No paths found in the schema."}]

    results = []
    async with httpx.AsyncClient() as client:
        tasks = []
        for path, path_item in paths.items():
            # Determine which method to test with: GET > HEAD > OPTIONS
            if "get" in path_item:
                method = "GET"
            elif "head" in path_item:
                method = "HEAD"
            elif "options" in path_item:
                method = "OPTIONS"
            else:
                # Skip if no suitable simple method is available
                continue

            tasks.append(test_single_endpoint(client, base_url, path, method))

        results = await asyncio.gather(*tasks)

    return results
