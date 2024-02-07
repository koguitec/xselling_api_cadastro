import json

from fastapi import Header, Query
from fastapi.responses import Response

from application.rest.schema.transaction import (
    TransactionRequest,
    TransactionResponse,
    TransactionResponseList,
)
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


async def transaction_create(
    transaction: TransactionRequest,
    authorization: str = Header(default=None),
) -> list[TransactionResponse]:

    try:
        client = auth_token.decode_jwt(authorization)
    except auth_token.jwt.ExpiredSignatureError as e:
        return Response(
            json.dumps({'error': str(e)}),
            media_type='application/json',
            status_code=401,
        )

    transaction_dict = transaction.model_dump()
    transaction_dict['client_id'] = client['client_id']

    request_obj = build_transaction_create_request(transaction_dict)

    repo = PostgresRepoTransaction()
    response = transaction_create_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=TransactionJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )


async def transaction_list(
    authorization: str = Header(default=None),
    id__eq: str = Query(None, alias='filter_id__eq'),
    code__eq: str = Query(None, alias='filter_code__eq'),
    ativo__eq: bool = Query(None, alias='filter_ativo__eq'),
    produto_id__eq: bool = Query(None, alias='filter_produto_id__eq'),
    page__eq: int = Query(None, alias='filter_page__eq'),
    items_per_page__eq: int = Query(None, alias='filter_items_per_page__eq'),
) -> TransactionResponseList:

    try:
        client = auth_token.decode_jwt(authorization)
    except auth_token.jwt.ExpiredSignatureError:
        raise

    qrystr_params = {
        'filters': {},
    }

    filters = {
        'id__eq': id__eq,
        'code__eq': code__eq,
        'ativo__eq': ativo__eq,
        'produto_id__eq': produto_id__eq,
        'client_id__eq': client['client_id'],
        'page__eq': page__eq,
        'items_per_page__eq': items_per_page__eq,
    }

    for arg, values in filters.items():
        if values is not None:
            qrystr_params['filters'][arg] = values

    request_obj = build_transaction_list_request(qrystr_params['filters'])

    repo = PostgresRepoTransaction()
    response = transaction_list_use_case(repo, request_obj)

    return Response(
        json.dumps(response.value, cls=TransactionJsonEncoder),
        media_type='application/json',
        status_code=STATUS_CODE[response.type],
    )
