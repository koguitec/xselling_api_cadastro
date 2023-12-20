# pylint: disable=c0116
import json
from unittest import mock

import pytest

from src.responses import ResponseSuccess


@pytest.fixture
def client_dict():
    return {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'razao_social': 'My company 1',
        'cnpj': '00.000.000/0000-01',
        'email': 'mycompany_1@email.com',
        'ativo': False,
    }


@mock.patch('application.rest.client.client_update_use_case')
def test_update(mock_use_case, client, client_dict):
    mock_use_case.return_value = ResponseSuccess(client_dict)

    http_response = client.put('/clients', json=client_dict)

    assert json.loads(http_response.data.decode('utf-8')) == client_dict

    mock_use_case.assert_called()

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.client.client_update_use_case')
def test_post_without_body(mock_use_case, client, client_dict):
    mock_use_case.return_value = ResponseSuccess(client_dict)

    http_response = client.post('/clients', json={})

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.client.client_update_use_case')
def test_post_with_missing_data(mock_use_case, client, client_dict):
    mock_use_case.return_value = ResponseSuccess(client_dict)

    client_dict.pop('id')
    client_dict_missing_data = client_dict

    http_response = client.post('/clients', json=client_dict_missing_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.client.client_update_use_case')
def test_post_with_extra_data(mock_use_case, client, client_dict):
    mock_use_case.return_value = ResponseSuccess(client_dict)

    client_dict.update({'extra': 'field'})
    client_dict_extra_data = client_dict

    http_response = client.post('/clients', json=client_dict_extra_data)

    assert 'error' in http_response.text
    assert http_response.status_code == 400
    assert http_response.mimetype == 'application/json'
