"""Modulo para adaptação do objeto request do framework específico para o
core da aplicação
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from fastapi import Request


@dataclass
class HttpRequest:
    headers: str = None
    data: str = None
    json: str = None
    query_params: str = None
    path_params: str = None
    url: str = None


class HttpStatusCode(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    SERVER_ERROR = 500


@dataclass
class HttpResponse:
    body: str
    status_code: int = HttpStatusCode


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
        json=await request.json()
        if request.method in ['POST', 'PUT']
        else None,
        query_params=request.query_params,
        path_params=request.path_params,
        url=request.url,
    )

    return http_request


async def request_adapter_recommendation(
    request: Request, controller: Callable
) -> HttpResponse:
    """Adapter for the request object. The ideia isa to create a layers to
    receive a request object no metter the web framework used: Flask, Django, FastAPI

    Args:
        request (Object): The actual web framework request object

    Returns:
        HttpRequest: Instance of HttpRequest
    """
    http_request = HttpRequest(
        headers=request.headers,
        data=request.body,
        json=await request.json() if request.method == 'POST' else None,
        query_params=request.query_params,
        path_params=request.path_params,
        url=request.url,
    )

    http_response = controller(http_request)

    return http_response
