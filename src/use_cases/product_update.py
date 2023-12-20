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
        product = repo.update_product(request.data)
        return ResponseSuccess(product)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
