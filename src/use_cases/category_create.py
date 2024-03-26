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
        category_exists = repo.list_category(
            filters={
                'descricao__in': [data['descricao'] for data in request.data],
            }
        )
        if category_exists:
            categories = [category.descricao for category in category_exists]
            return ResponseFailure(
                ResponseTypes.DOMAIN_ERROR,
                f'Categoria(s): {categories} já cadastrada(s)',
            )
        client = repo.create_category(request.data)
        return ResponseSuccess(client, type_='insertion')
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
