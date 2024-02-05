import json

from fastapi import Request
from fastapi.responses import Response

from application.rest.schema.category import (
    CategoryRequest,
    CategoryResponse,
    UpdateCategoryRequest,
)
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


async def category_create(category: CategoryRequest) -> CategoryResponse:
    request_obj = build_create_category_request(category.model_dump())

    repo = PostgresRepoCategory()
    response = category_create_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=CategoryJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def category_list(request: Request) -> list[CategoryResponse]:
    http_request: HttpRequest = await request_adapter(request)
    qrystr_params = {
        'filters': {},
    }

    try:
        token = http_request.headers
        client = auth_token.decode_jwt(token['Authorization'])
    except auth_token.jwt.ExpiredSignatureError:
        raise

    qrystr_params['filters'].update({'client_id__eq': client['client_id']})

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


async def category_update(category: UpdateCategoryRequest) -> CategoryResponse:
    request_obj = build_update_category_request(category.model_dump())

    repo = PostgresRepoCategory()
    response = category_update_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=CategoryJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )
