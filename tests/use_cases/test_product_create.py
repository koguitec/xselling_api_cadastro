from unittest import mock

import pytest

from src.requests.product_create import build_create_product_request
from src.use_cases.product_create import product_create_use_case


@pytest.fixture
def product_dict():
    return {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'nome': 'My product',
        'descricao': 'My descricao',
        'sky': '0123456789',
        'categoria_id': 1,
        'dt_criacao': '01/01/2023 00:00:00',
        'dt_alteracao': '01/01/2023 00:00:00',
        'ativo': True,
    }


def test_create_product(product_dict):
    repo = mock.Mock()
    repo.list_product.return_value = []
    repo.create_product.return_value = product_dict

    new_product = {
        'nome': 'My product',
        'descricao': 'My descricao',
        'sku': '0123456789',
        'categoria_id': 1,
    }

    request = build_create_product_request(new_product)

    result = product_create_use_case(repo, request)

    assert bool(result) is True
    repo.create_product.assert_called_with(new_product)
    assert result.value == product_dict
