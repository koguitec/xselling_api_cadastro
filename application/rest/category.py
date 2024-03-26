import json

from fastapi import Header, Query, Request
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from application.rest.schema.category import (
    CategoryRequest,
    CategoryResponse,
    CategoryResponseList,
    UpdateCategoryRequest,
)
from src.errors.error_handler import handle_errors
from src.plugins.jwt_plugin import auth_token
from src.repository.postgres.postgresrepo_category import PostgresRepoCategory
from src.requests.category_create import build_create_category_request
from src.requests.category_list import build_category_list_request
from src.requests.category_update import build_update_category_request
from src.responses import STATUS_CODE
from src.serializers.category import CategoryJsonEncoder
from src.use_cases.category_create import category_create_use_case
from src.use_cases.category_list import category_list_use_case
from src.use_cases.category_update import category_update_use_case

from .adapters.request_adapter import HttpRequest, request_adapter
from .utils.validation_reponse import format_pydantic_error


async def category_create(request: Request) -> CategoryResponse:

    http_request: HttpRequest = await request_adapter(request)

    try:
        data = CategoryRequest.model_validate(http_request.json).model_dump()
        data['client'] = auth_token.decode_jwt(http_request)
    except Exception as exc:
        http_response = handle_errors(exc)
        return JSONResponse(http_response.body, http_response.status_code)

    request_obj = build_create_category_request(data)
    repo = PostgresRepoCategory()
    response = category_create_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=CategoryJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def category_list(request: Request) -> CategoryResponseList:
    http_request: HttpRequest = await request_adapter(request)

    try:
        client = auth_token.decode_jwt(http_request)
    except Exception as exc:
        http_response = handle_errors(exc)
        return JSONResponse(http_response.body, http_response.status_code)

    qrystr_params = {
        'filters': {},
    }

    qrystr_params['filters']['client_id'] = client['client_id']

    for arg, values in http_request.query_params.items():
        if arg.startswith('filter_'):
            qrystr_params['filters'][arg.replace('filter_', '')] = values

    request_obj = build_category_list_request(filters=qrystr_params['filters'])
    repo = PostgresRepoCategory()
    response = category_list_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=CategoryJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def category_update(request: Request) -> CategoryResponse:

    http_request: HttpRequest = await request_adapter(request)

    try:
        data = UpdateCategoryRequest.model_validate(
            http_request.json
        ).model_dump()
        data['client'] = auth_token.decode_jwt(http_request)
    except Exception as exc:
        http_response = handle_errors(exc)
        return JSONResponse(http_response.body, http_response.status_code)

    request_obj = build_update_category_request(data.model_dump())
    repo = PostgresRepoCategory()
    response = category_update_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=CategoryJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )
