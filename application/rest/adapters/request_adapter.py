"""Modulo para adaptação do objeto request do framework específico para o
core da aplicação
"""

from fastapi import Request


class HttpRequest:
    def __init__(
        self,
        headers=None,
        data=None,
        json=None,
        query_params=None,
        path_params=None,
        url=None,
    ) -> None:
        self.headers = headers
        self.data = data
        self.body = json
        self.query_params = query_params
        self.path_params = path_params
        self.url = url


async def request_adapter(request: Request) -> HttpRequest:
    """Adapter for the request object. The ideia isa to create a layers to
    receive a request object no metter the web framework used: Flask, Django, FastAPI

    Args:
        request (Object): The actual web framework request object

    Returns:
        HttpRequest: Instance of HttpRequest
    """
    http_request = HttpRequest(
        headers=request.headers,
        data=await request.body(),
        json=await request.json() if request.method == 'POST' else None,
        query_params=request.query_params,
        path_params=request.path_params,
        url=request.url,
    )

    return http_request
