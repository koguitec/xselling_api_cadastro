import json

from fastapi import Header, Query, Request
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from application.rest.cache_service.cache_service import CacheService
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
from .utils.validation_reponse import format_pydantic_error


async def product_create(request: Request) -> ProductResponse:

    http_request: HttpRequest = await request_adapter(request)

    try:
        data = ProductSchema.model_validate(json.loads(http_request.data))
        client = auth_token.decode_jwt(http_request.headers['Authorization'])
    except ValidationError as e:
        return JSONResponse(
            format_pydantic_error(e),
            media_type='application/json',
            status_code=422,
        )
    except auth_token.jwt.ExpiredSignatureError as e:
        return Response(
            json.dumps({'error': str(e)}),
            media_type='application/json',
            status_code=401,
        )

    request_obj = build_create_product_request(data.model_dump())

    repo = PostgresRepoProduct()
    response = product_create_use_case(repo, request_obj)

    if response.type == 200:
        CacheService.update_client_items(client['client_id'])

    return Response(
        json.dumps(response.value, cls=ProductJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def product_list(request: Request) -> ProductResponseList:
    http_request: HttpRequest = await request_adapter(request)

    try:
        client = auth_token.decode_jwt(http_request.headers['Authorization'])
    except auth_token.jwt.ExpiredSignatureError as e:
        return Response(
            json.dumps({'error': str(e)}),
            media_type='application/json',
            status_code=401,
        )

    qrystr_params = {
        'filters': {},
    }

    qrystr_params['filters']['client_id'] = client['client_id']

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


async def product_update(request: Request) -> ProductResponse:

    http_request: HttpRequest = await request_adapter(request)

    try:
        data = UpdateProductSchema.model_validate(
            json.loads(http_request.data)
        )
        client = auth_token.decode_jwt(http_request.headers['Authorization'])
    except ValidationError as e:
        return JSONResponse(
            format_pydantic_error(e),
            media_type='application/json',
            status_code=422,
        )
    except auth_token.jwt.ExpiredSignatureError as e:
        return Response(
            json.dumps({'error': str(e)}),
            media_type='application/json',
            status_code=401,
        )

    request_obj = build_update_product_request(data.model_dumps())

    repo = PostgresRepoProduct()
    response = product_update_use_case(repo, request_obj)

    if response.type == 200:
        CacheService.update_client_items(client['client_id'])

    return Response(
        json.dumps(response.value, cls=ProductJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )
