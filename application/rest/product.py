import json

from fastapi import Header, Query, Request
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError

from application.rest.cache_service.cache_service import CacheService
from application.rest.schema.product import (
    ProductRequest,
    ProductResponse,
    ProductResponseList,
    UpdateProductRequest,
)
from src.errors.error_handler import handle_errors
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
        data = ProductRequest.model_validate(http_request.json).model_dump()
        data['client'] = auth_token.decode_jwt(http_request)
    except Exception as exc:
        http_response = handle_errors(exc)
        return JSONResponse(http_response.body, http_response.status_code)

    request_obj = build_create_product_request(data)
    repo = PostgresRepoProduct()
    response = product_create_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=ProductJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def product_list(request: Request) -> ProductResponseList:
    http_request: HttpRequest = await request_adapter(request)

    try:
        client = auth_token.decode_jwt(http_request)
    except Exception as exc:
        http_response = handle_errors(exc)
        return JSONResponse(http_response.body, http_response.status_code)

    qrystr_params = {
        'filters': {},
    }

    qrystr_params['filters']['client_id__eq'] = client['client_id']

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
        data = UpdateProductRequest.model_validate(
            http_request.json
        ).model_dump()
        data['client'] = auth_token.decode_jwt(http_request)
    except Exception as exc:
        http_response = handle_errors(exc)
        return JSONResponse(http_response.body, http_response.status_code)

    request_obj = build_update_product_request(data)
    repo = PostgresRepoProduct()
    response = product_update_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=ProductJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )
