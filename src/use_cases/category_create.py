from src.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
    build_response_from_invalid_request,
)


def category_create_use_case(repo, request):
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
        check_category_exists = repo.list_category(
            filters={
                'client_id': request.data['client_id'],
                'descricao__eq': request.data['descricao'],
            }
        )
        if check_category_exists:
            return ResponseFailure(
                ResponseTypes.DOMAIN_ERROR, 'Categoria já cadastrada'
            )
        client = repo.create_category(request.data)
        return ResponseSuccess(client)
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
