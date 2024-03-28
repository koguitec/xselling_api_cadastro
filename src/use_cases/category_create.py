from application.rest.cache_service.cache_service import CacheService
from src.repository.postgres.postgresrepo_product import PostgresRepoProduct
from src.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
    build_response_from_invalid_request,
)


def category_create_use_case(repo: PostgresRepoProduct, request):
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
        categories: list = request.data['categories']
        client_id: str = request.data['client']['client_id']

        category_exists = repo.list_category(
            filters={
                'descricao__in': [
                    category['descricao'] for category in categories
                ],
                'client_id__eq': client_id
            }
        )
        if category_exists:
            categories_names = [
                category.descricao for category in category_exists
            ]
            return ResponseFailure(
                ResponseTypes.DOMAIN_ERROR,
                f'Categoria(s): {categories_names} já cadastrada(s)',
            )
        result = repo.create_category(categories)
        return ResponseSuccess(result, type_='insertion')
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
