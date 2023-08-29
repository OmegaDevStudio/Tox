from typing import Awaitable, Optional
import asyncio
import aiohttp
import ujson
import uvloop

uvloop.install()


class RequestHandler:
    """Request Handler class, used to create mass request"""

    def __init__(self, base_url: Optional[str] = None, *args, **kwargs) -> None:
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            *args,
            **kwargs,
            connector=aiohttp.TCPConnector(
                keepalive_timeout=10,
                ttl_dns_cache=204,
                limit=0,
                limit_per_host=0,
            ),
            json_serialize=ujson.dumps,
            auto_decompress=True,
        )
        if base_url is not None:
            self.root = base_url

    async def request(
        self, method: str, url: str, *args, **kwargs
    ) -> aiohttp.ClientResponse:
        """Generates a request"""
        return await self.session.request(method, self.root + url, *args, **kwargs)

    async def gather_requests(
        self, reqs: list[Awaitable]
    ) -> list[aiohttp.ClientResponse]:
        """Runs multiple requests asynchronously"""

        return await asyncio.gather(*(asyncio.create_task(req) for req in reqs))

    async def json(self, resp: aiohttp.ClientResponse) -> dict:
        """Generates json response from request"""
        return await resp.json()

    async def text(self, resp: aiohttp.ClientResponse) -> dict:
        """Generates text response from request"""
        return await resp.text()

    async def gather_json(
        self, resps: list[aiohttp.ClientResponse]
    ) -> list[str | dict]:
        """Runs multiple asynchronous json responses"""
        try:
            return await asyncio.gather(
                *(asyncio.create_task(self.json(resp)) for resp in resps)
            )
        except aiohttp.client_exceptions.ContentTypeError:
            return await asyncio.gather(
                *(asyncio.create_task(self.text(resp)) for resp in resps)
            )

    async def close(self):
        """Closes client session"""
        return await self.session.close()

    async def __aenter__(self):
        """Enters context manager"""
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        """Exits context manager"""
        return await self.close()
