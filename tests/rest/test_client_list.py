import json
from unittest import mock

import pytest

from src.domain.client import Client
from src.responses import ResponseFailure, ResponseSuccess, ResponseTypes

client_dict = {
    'id': 1,
    'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
    'razao_social': 'My company 1',
    'cnpj': '00.000.000/0000-01',
    'email': 'mycompany_1@email.com',
    'dt_inclusao': '01/01/2023 00:00:00',
    'dt_alteracao': '01/01/2023 00:00:00',
    'ativo': True,
}

clients = [Client.from_dict(client_dict)]


@mock.patch('application.rest.client.client_list_use_case')
def test_get(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(clients)

    http_response = client.get('/clients')

    assert json.loads(http_response.data.decode('utf-8')) == [client_dict]

    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args
    assert args[1].filters == {}

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@mock.patch('application.rest.client.client_list_use_case')
def test_get_with_filters(mock_use_case, client):
    mock_use_case.return_value = ResponseSuccess(clients)

    http_response = client.get('/clients?filter_ativo__eq=true')

    assert json.loads(http_response.data.decode('utf-8')) == [client_dict]

    mock_use_case.assert_called()
    args, kwargs = mock_use_case.call_args

    assert args[1].filters == {'ativo__eq': 'true'}

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@pytest.mark.parametrize(
    'response_type, expected_status_code',
    [
        (ResponseTypes.PARAMETERS_ERROR, 400),
        (ResponseTypes.RESOURCE_ERROR, 404),
        (ResponseTypes.SYSTEM_ERROR, 500),
    ],
)
@mock.patch('application.rest.client.client_list_use_case')
def test_get_response_failures(
    mock_use_case, client, response_type, expected_status_code
):
    mock_use_case.return_value = ResponseFailure(
        response_type, message='Just an error message'
    )

    http_response = client.get('/clients?dummy_request_string')

    mock_use_case.assert_called()

    assert http_response.status_code == expected_status_code
