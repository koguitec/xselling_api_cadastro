"""Module for the product update use case"""
from src.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
    build_response_from_invalid_request,
)


def product_update_use_case(repo, request):
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
        product: list = request.data
        client: str = request.data.pop('client')

        product_exists = repo.list_product(
            filters={
                'id__eq': product['id'],
                'sku__eq': product['sku'],
                'client_id__eq': client['client_id'],
            }
        )

        if len(product_exists) == 0:
            return ResponseFailure(
                ResponseTypes.DOMAIN_ERROR,
                f'Produto: {product["nome"]} não encontrado',
            )

        product = repo.update_product(product)
        return ResponseSuccess(product)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
