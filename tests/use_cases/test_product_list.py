"""Test module for product list use cases"""
# pylint: disable=w0621
from unittest import mock

import pytest

from src.domain.product import Product
from src.requests.product_list import build_product_list_request
from src.responses import ResponseTypes
from src.use_cases.product_list import product_list_use_case


@pytest.fixture
def domain_products():
    product_1 = Product(
        id=1,
        code='0000-0000-0000-0000-0000-0000',
        nome='Produto A',
        descricao='Descrição A',
        sku='0123456789',
        categoria_id=1,
        dt_inclusao='01/01/2023 00:00:00',
        dt_alteracao='01/01/2023 00:00:00',
        ativo=True,
    )
    product_2 = Product(
        id=1,
        code='0000-0000-0000-0000-0000-0000',
        nome='Produto B',
        descricao='Descrição B',
        sku='0123456789',
        categoria_id=1,
        dt_inclusao='01/01/2023 00:00:00',
        dt_alteracao='01/01/2023 00:00:00',
        ativo=True,
    )
    product_3 = Product(
        id=1,
        code='0000-0000-0000-0000-0000-0000',
        nome='Produto C',
        descricao='Descrição C',
        sku='0123456789',
        categoria_id=1,
        dt_inclusao='01/01/2023 00:00:00',
        dt_alteracao='01/01/2023 00:00:00',
        ativo=True,
    )
    product_4 = Product(
        id=1,
        code='0000-0000-0000-0000-0000-0000',
        nome='Produto D',
        descricao='Descrição D',
        sku='0123456789',
        categoria_id=1,
        dt_inclusao='01/01/2023 00:00:00',
        dt_alteracao='01/01/2023 00:00:00',
        ativo=True,
    )

    return [product_1, product_2, product_3, product_4]


def test_product_list_without_parameters(domain_products):
    repo = mock.Mock()
    repo.list_product.return_value = domain_products

    request = build_product_list_request()

    response = product_list_use_case(repo, request)

    assert bool(response) is True
    repo.list_product.assert_called_with(filters=None)
    assert response.value == domain_products


def test_product_list_with_filters(domain_products):
    repo = mock.Mock()
    repo.list_product.return_value = domain_products

    qry_filters = {'ativo__eq': True}
    request = build_product_list_request(filters=qry_filters)

    response = product_list_use_case(repo, request)

    assert bool(response) is True
    repo.list_product.assert_called_with(filters=qry_filters)
    assert response.value == domain_products


def test_product_list_handles_generic_error():
    repo = mock.Mock()
    repo.list_product.side_effect = Exception('Just an error message')

    request = build_product_list_request(filters={})

    response = product_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.SYSTEM_ERROR,
        'message': 'Exception: Just an error message',
    }


def test_product_list_handles_bad_request():
    repo = mock.Mock()

    request = build_product_list_request(filters=5)

    response = product_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.PARAMETERS_ERROR,
        'message': 'filters: Is not iterable',
    }
