import json

from fastapi import Header, Query
from fastapi.responses import Response

from application.rest.schema.product import (
    ProductResponse,
    ProductResponseList,
    ProductSchema,
    UpdateProductSchema,
)
from src.plugins.jwt_plugin import auth_token
from src.repository.postgres.postgresrepo_product import PostgresRepoProduct
from src.requests.product_create import build_create_product_request
from src.requests.product_list import build_product_list_request
from src.requests.product_update import build_update_product_request
from src.responses import STATUS_CODE
from src.serializers.product import ProductJsonEncoder
from src.use_cases.product_create import product_create_use_case
from src.use_cases.product_list import product_list_use_case
from src.use_cases.product_update import product_update_use_case

from .adapters.request_adapter import HttpRequest, request_adapter


async def product_create(product: ProductSchema) -> ProductResponse:
    request_obj = build_create_product_request(product.model_dumps())

    repo = PostgresRepoProduct()
    response = product_create_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=ProductJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def product_list(
    authorization: str = Header(default=None),
    id__eq: str = Query(None, alias='filter_id__eq'),
    code__eq: str = Query(None, alias='filter_code__eq'),
    ativo__eq: bool = Query(None, alias='filter_ativo__eq'),
    page__eq: int = Query(None, alias='filter_page__eq'),
    items_per_page__eq: int = Query(None, alias='filter_items_per_page__eq'),
) -> ProductResponseList:

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
        'page__eq': page__eq,
        'items_per_page__eq': items_per_page__eq,
    }

    for arg, values in filters.items():
        if values is not None:
            qrystr_params['filters'][arg] = values

    request_obj = build_product_list_request(qrystr_params['filters'])

    repo = PostgresRepoProduct()
    response = product_list_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=ProductJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def product_update(product: UpdateProductSchema) -> ProductResponse:
    request_obj = build_update_product_request(product.model_dumps())

    repo = PostgresRepoProduct()
    response = product_update_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=ProductJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )
