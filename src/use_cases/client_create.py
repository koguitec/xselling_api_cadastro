"""Module for the client create use case"""
from src.domain.auth_jwt import AuthJwt
from src.domain.client import Client
from src.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
    build_response_from_invalid_request,
)
from src.use_cases.token_create import create_token


def client_create_use_case(repo, request):
    """Use case logic

    Args:
        repo (Object): Repository object
        request (Object): Validated request

    Returns:
        ResponseSuccess: If no errors

    Exceptions:
        ResponseFailure: If errors
    """
    if not request:
        return build_response_from_invalid_request(request)
    try:
        check_client_exists = repo.list_client(
            filters={'cnpj__eq': request.data.cnpj}
        )
        if check_client_exists:
            return ResponseFailure(
                ResponseTypes.DOMAIN_ERROR, 'O CNPJ já existe'
            )
        client: Client = repo.create_client(request.data)

        # Create token
        auth_token: AuthJwt = create_token(client)

        repo.create_token(auth_token.to_dict())

        return ResponseSuccess(client)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
