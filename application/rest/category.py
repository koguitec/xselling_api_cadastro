import json

from fastapi import Header, Query
from fastapi.responses import Response

from application.rest.schema.category import (
    CategoryRequest,
    CategoryResponse,
    CategoryResponseList,
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


async def category_list(
    authorization: str = Header(default=None),
    id__eq: str = Query(None, alias='filter_id__eq'),
    code__eq: str = Query(None, alias='filter_code__eq'),
    ativo__eq: bool = Query(None, alias='filter_ativo__eq'),
    descricao__eq: str = Query(None, alias='filter_descricao__eq'),
    page__eq: int = Query(None, alias='filter_page__eq'),
    items_per_page__eq: int = Query(None, alias='filter_items_per_page__eq'),
) -> CategoryResponseList:

    try:
        client = auth_token.decode_jwt(authorization)
    except auth_token.jwt.ExpiredSignatureError as e:
        return Response(
            json.dumps({'error': str(e)}),
            media_type='application/json',
            status_code=401,
        )

    qrystr_params = {
        'filters': {},
    }

    filters = {
        'id__eq': id__eq,
        'code__eq': code__eq,
        'ativo__eq': ativo__eq,
        'client_id__eq': client['client_id'],
        'descricao__eq': descricao__eq,
        'page__eq': page__eq,
        'items_per_page__eq': items_per_page__eq,
    }

    for arg, values in filters.items():
        if values is not None:
            qrystr_params['filters'][arg] = values

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
