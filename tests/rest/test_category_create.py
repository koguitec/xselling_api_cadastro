import json
from unittest import mock

from src.responses import ResponseSuccess

category_dict = {
    'descricao': 'Descricao A',
    'client_id': 1,
}


@mock.patch('application.rest.category.category_create_use_case')
def test_post(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(category_dict)

    http_response = client.post('/categories', json=category_dict)

    assert json.loads(http_response.data.decode('utf-8')) == category_dict

    mock_use_case.assert_called()

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.category.category_create_use_case')
def test_post_without_body(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(category_dict)

    http_response = client.post('/categories', json={})

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.category.category_create_use_case')
def test_post_with_missing_data(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(category_dict)

    category_dict.pop('descricao')
    category_dict_missing_data = category_dict

    http_response = client.post('/categories', json=category_dict_missing_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.category.category_create_use_case')
def test_post_with_extra_data(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(category_dict)

    category_dict.update({'extra': 'field'})
    category_dict_extra_data = category_dict

    http_response = client.post('/categories', json=category_dict_extra_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'
