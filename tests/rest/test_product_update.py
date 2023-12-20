# pylint: disable=c0116
import json
from unittest import mock

import pytest

from src.responses import ResponseSuccess


@pytest.fixture
def product_dict():
    return {
        'id': 1,
        'nome': 'Produto A',
        'descricao': 'Descricao A',
        'sku': '0123456789',
        'ativo': True,
    }


@mock.patch('application.rest.product.product_update_use_case')
def test_put(mock_use_case, client, product_dict):
    mock_use_case.return_value = ResponseSuccess(product_dict)

    http_response = client.put('/products', json=product_dict)

    assert json.loads(http_response.data.decode('utf-8')) == product_dict

    mock_use_case.assert_called()

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.product.product_update_use_case')
def test_put_without_body(mock_use_case, client, product_dict):
    mock_use_case.return_value = ResponseSuccess(product_dict)

    http_response = client.put('/products', json={})

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.product.product_update_use_case')
def test_put_with_missing_data(mock_use_case, client, product_dict):
    mock_use_case.return_value = ResponseSuccess(product_dict)

    product_dict.pop('id')
    product_dict_missing_data = product_dict

    http_response = client.put('/products', json=product_dict_missing_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.product.product_update_use_case')
def test_put_with_extra_data(mock_use_case, client, product_dict):
    mock_use_case.return_value = ResponseSuccess(product_dict)

    product_dict.update({'extra': 'field'})
    product_dict_missing_data = product_dict

    http_response = client.put('/products', json=product_dict_missing_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'
