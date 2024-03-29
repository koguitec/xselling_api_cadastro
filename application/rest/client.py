import json

from fastapi import Request
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from application.rest.schema.client import (
    ClientRequest,
    ClientResponse,
    ClientResponseList,
    UpdateClientRequest,
)
from src.domain.client import Client
from src.errors.error_handler import handle_errors
from src.repository.postgres.postgresrepo_client import PostgresRepoClient
from src.requests.client_create import build_create_client_request
from src.requests.client_list import build_client_list_request
from src.requests.client_update import build_update_client_request
from src.responses import STATUS_CODE
from src.serializers.auth_jwt import ClientAuthJsonEncoder
from src.serializers.client import ClientJsonEncoder
from src.use_cases.client_create import client_create_use_case
from src.use_cases.client_list import client_list_use_case
from src.use_cases.client_update import client_update_use_case

from .adapters.request_adapter import HttpRequest, request_adapter
from .utils.validation_reponse import format_pydantic_error


async def client_create(request: Request) -> ClientResponse:

    http_request: HttpRequest = await request_adapter(request)

    try:
        data = ClientRequest.model_validate(http_request.json).model_dump()
    except Exception as exc:
        http_response = handle_errors(exc)
        return JSONResponse(http_response.body, http_response.status_code)

    client_domain = Client.from_dict(data)
    request_obj = build_create_client_request(client_domain)
    repo = PostgresRepoClient()
    response = client_create_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=ClientAuthJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def client_list(request: Request) -> ClientResponseList:
    http_request: HttpRequest = await request_adapter(request)

    qrystr_params = {
        'filters': {},
    }

    for arg, values in http_request.query_params.items():
        if arg.startswith('filter_'):
            qrystr_params['filters'][arg.replace('filter_', '')] = values

    request_obj = build_client_list_request(filters=qrystr_params['filters'])

    repo = PostgresRepoClient()
    response = client_list_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=ClientJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def client_update(request: Request) -> ClientResponse:

    http_request: HttpRequest = await request_adapter(request)

    try:
        data = UpdateClientRequest.model_validate(
            http_request.json
        ).model_dump()
    except Exception as exc:
        http_response = handle_errors(exc)
        return JSONResponse(http_response.body, http_response.status_code)

    client_domain = Client.from_dict(data)
    request_obj = build_update_client_request(client_domain)

    repo = PostgresRepoClient()
    response = client_update_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=ClientJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )
