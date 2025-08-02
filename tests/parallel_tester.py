import time
from typing import List, Tuple

import anyio
import httpx


async def run_parallel_tests(
    endpoints: List[str], rate_limit: int, per_second: int
) -> List[Tuple[str, int, float]]:
    """
    Tests a list of endpoints in parallel with rate limiting.

    Args:
        endpoints: A list of endpoints to test.
        rate_limit: The maximum number of requests per `per_second`.
        per_second: The time window for the rate limit in seconds.

    Returns:
        A list of tuples containing the endpoint, the status code, and the
        response time.
    """
    results = []
    sleep_time = per_second / rate_limit

    async def _make_request(
        client: httpx.AsyncClient,
        endpoint: str,
        results: List[Tuple[str, int, float]],
    ) -> None:
        """
        Makes a request to an endpoint and appends the result to a list.

        Args:
            client: The httpx client.
            endpoint: The endpoint to make the request to.
            results: The list to append the results to.
        """
        start_time = time.time()
        response = await client.get(endpoint)
        end_time = time.time()
        results.append((endpoint, response.status_code, end_time - start_time))
        await anyio.sleep(sleep_time)

    async with httpx.AsyncClient() as client:
        async with anyio.create_task_group() as tg:
            for endpoint in endpoints:
                tg.start_soon(_make_request, client, endpoint, results)
    return results
