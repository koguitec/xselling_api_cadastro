from application.rest.cache_service.cache_service import CacheService
from src.repository.postgres.postgresrepo_product import PostgresRepoProduct
from src.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
    build_response_from_invalid_request,
)


def product_create_use_case(repo: PostgresRepoProduct, request):
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
        products: list = request.data['products']
        client_id: str = request.data['client']['client_id']

        product_exists = repo.list_product(
            filters={
                'sku__in': [product['sku'] for product in products],
            }
        )

        if product_exists:
            products_names = [product.nome for product in product_exists]
            return ResponseFailure(
                ResponseTypes.DOMAIN_ERROR,
                f'Produto(s): {products_names} já cadastrado(s)',
            )

        result = repo.create_product(products)
        CacheService().update_client_items_in_cache(
            client_id=client_id, items=products
        )

        return ResponseSuccess(result, type_='insertion')
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
