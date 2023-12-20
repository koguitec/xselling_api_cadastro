from unittest import mock

import pytest

from src.requests.product_update import build_update_product_request
from src.use_cases.product_update import product_update_use_case


@pytest.fixture
def product_to_update():
    return {
        'id': 1,
        'nome': 'Produto A',
        'descricao': 'Descricao A',
        'sku': '0123456789',
        'ativo': False,
    }


def test_update_product_success(product_to_update):
    repo = mock.Mock()

    repo.update_product.return_value = product_to_update

    request = build_update_product_request(product_to_update)

    result = product_update_use_case(repo, request)

    assert bool(result) is True
    repo.update_product.assert_called_with(product_to_update)
