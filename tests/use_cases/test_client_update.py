from unittest import mock

import pytest

from src.requests.client_update import build_update_client_request
from src.responses import ResponseTypes
from src.use_cases.client_update import client_update_use_case


@pytest.fixture
def client_to_update():
    return {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'razao_social': 'My company 1',
        'cnpj': '00.000.000/0000-01',
        'email': 'mycompany_1@email.com',
        'dt_criacao': '01/01/2023 00:00:00',
        'dt_alteracao': '01/01/2023 00:00:00',
        'ativo': False,
    }


def test_update_client_success(client_to_update):
    repo = mock.Mock()

    repo.update_client.return_value = client_to_update

    request = build_update_client_request(client_to_update)

    response = client_update_use_case(repo, request)

    assert bool(response) is True
    repo.update_client.assert_called_with(client_to_update)
    assert response.value == client_to_update


@pytest.mark.skip('olhar depois')
def test_update_client_handles_generic_error():
    repo = mock.Mock()
    repo.update_client.side_effect = Exception('Just an error message')

    new_client = {
        'razao_social': 'New Company',
        'cnpj': '',
        'email': 'new_company@email.com',
        'ativo': True,
    }

    request = build_update_client_request(client=new_client)

    response = client_update_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.SYSTEM_ERROR,
        'message': 'Exception: Just an error message',
    }


def test_update_client_handles_cnjp_validation_error():
    repo = mock.Mock()

    invalid_client_data = {
        'razao_social': 'New Company',
        'cnpj': 'invalid_cnpj_format',
        'email': 'new_company@email.com',
        'ativo': True,
    }

    request = build_update_client_request(invalid_client_data)

    response = client_update_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.PARAMETERS_ERROR,
        'message': 'value: Invalid CNPJ',
    }


def test_updaet_client_handles_email_validation_error():
    repo = mock.Mock()

    invalid_client_data = {
        'razao_social': 'New Company',
        'cnpj': '11.111.111/1111-11',
        'email': 'invalid_email_format',
        'ativo': True,
    }

    request = build_update_client_request(invalid_client_data)

    response = client_update_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.PARAMETERS_ERROR,
        'message': 'value: Invalid e-mail',
    }
