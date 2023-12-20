import json
from unittest import mock

from src.responses import ResponseSuccess

product_dict = {
    'nome': 'My product',
    'descricao': 'My description',
    'sku': '0123456789',
    'categoria_id': 1,
}


@mock.patch('application.rest.product.product_create_use_case')
def test_post(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(product_dict)

    http_response = client.post('/products', json=product_dict)

    assert json.loads(http_response.data.decode('utf-8')) == product_dict

    mock_use_case.assert_called()

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.product.product_create_use_case')
def test_post_without_body(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(product_dict)

    http_response = client.post('/products', json={})

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.product.product_create_use_case')
def test_post_with_missing_data(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(product_dict)

    product_dict.pop('descricao')
    product_dict_missing_data = product_dict

    http_response = client.post('/products', json=product_dict_missing_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.product.product_create_use_case')
def test_post_with_extra_data(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(product_dict)

    product_dict.update({'extra': 'field'})
    product_dict_extra_data = product_dict

    http_response = client.post('/products', json=product_dict_extra_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'
