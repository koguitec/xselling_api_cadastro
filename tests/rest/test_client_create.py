import json
from unittest import mock

from src.responses import ResponseSuccess

client_dict = {
    'razao_social': 'My company 1',
    'cnpj': '00.000.000/0000-01',
    'email': 'mycompany_1@email.com',
}


@mock.patch('application.rest.client.client_create_use_case')
def test_post(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(client_dict)

    http_response = client.post('/clients', json=client_dict)

    assert json.loads(http_response.data.decode('utf-8')) == client_dict

    mock_use_case.assert_called()

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.client.client_create_use_case')
def test_post_without_body(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(client_dict)

    http_response = client.post('/clients', json={})

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.client.client_create_use_case')
def test_post_with_missing_data(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(client_dict)

    client_dict.pop('cnpj')
    client_dict_missing_data = client_dict

    http_response = client.post('/clients', json=client_dict_missing_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.client.client_create_use_case')
def test_post_with_extra_data(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(client_dict)

    client_dict.update({'extra': 'field'})
    client_dict_extra_data = client_dict

    http_response = client.post('/clients', json=client_dict_extra_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'
