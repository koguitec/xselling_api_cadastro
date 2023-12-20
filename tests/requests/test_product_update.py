from datetime import datetime

from src.requests.product_update import build_update_product_request


def test_build_product_update_request():
    product_to_update = {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'nome': 'Produto A',
        'descricao': 'Descricao A',
        'sku': '0123456789',
        'ativo': True,
    }

    request = build_update_product_request(product_to_update)

    assert bool(request) is True
    assert 'dt_alteracao' in product_to_update
    assert isinstance(product_to_update['dt_alteracao'], datetime)
