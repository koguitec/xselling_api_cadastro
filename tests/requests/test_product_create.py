import uuid

from src.requests.product_create import build_create_product_request


def test_build_product_create_request():
    product = {
        'nome': 'My product',
        'descricao': 'My description',
        'sky': '0123456789',
        'categoria_id': 1,
    }

    request = build_create_product_request(product)

    assert bool(request) is True
    assert 'code' in product
    assert isinstance(product['code'], uuid.UUID)
