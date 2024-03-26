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
        product_exists = repo.list_product(
            filters={
                'nome__in': [data['nome'] for data in request.data],
            }
        )
        if product_exists:
            products = [product.nome for product in product_exists]
            return ResponseFailure(
                ResponseTypes.DOMAIN_ERROR,
                f'Produto(s): {products} já cadastrado(s)',
            )
        product = repo.create_product(request.data)
        return ResponseSuccess(product, type_='insertion')
    except Exception as exc:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)
