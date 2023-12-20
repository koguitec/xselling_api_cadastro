import json

from fastapi import Request
from fastapi.responses import Response
from pydantic import ValidationError

from application.rest.schema.transaction import StoreTransactions
from src.plugins.jwt_plugin import auth_token
from src.repository.postgres.postgresrepo_transaction import (
    PostgresRepoTransaction,
)
from src.requests.transaction_create import build_transaction_create_request
from src.requests.transaction_list import build_transaction_list_request
from src.responses import STATUS_CODE
from src.serializers.transaction import TransactionJsonEncoder
from src.use_cases.transaction_create import transaction_create_use_case
from src.use_cases.transaction_list import transaction_list_use_case

from .adapters.request_adapter import HttpRequest, request_adapter


async def transaction_create(request: Request):
    http_request: HttpRequest = await request_adapter(request)

    try:
        token = http_request.headers
        client = auth_token.decode_jwt(token['Authorization'])
    except auth_token.jwt.ExpiredSignatureError:
        raise

    try:
        transaction = StoreTransactions.parse_raw(http_request.data)
    except ValidationError as e:
        return Response({'error': e.errors()}, 400)

    transaction_dict = transaction.dict()

    transaction_dict.update({'client_id': client['client_id']})

    request_obj = build_transaction_create_request(transaction_dict)

    repo = PostgresRepoTransaction()
    response = transaction_create_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=TransactionJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def transaction_list(request: Request):
    http_request: HttpRequest = await request_adapter(request)
    qrystr_params = {
        'filters': {},
    }

    for arg, values in http_request.query_params.items():
        if arg.startswith('filter_'):
            qrystr_params['filters'][arg.replace('filter_', '')] = values

    request_obj = build_transaction_list_request(qrystr_params['filters'])

    repo = PostgresRepoTransaction()
    response = transaction_list_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=TransactionJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )
