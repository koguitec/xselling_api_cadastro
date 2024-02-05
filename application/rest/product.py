import json

from fastapi import Request
from fastapi.responses import Response

from application.rest.schema.product import (
    ProductResponse,
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


async def product_list(request: Request) -> list[ProductResponse]:
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
