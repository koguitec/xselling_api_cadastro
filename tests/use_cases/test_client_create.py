"""Test module for create client"""
# pylint: disable=c0116
from unittest import mock

import pytest

from src.domain.client import Client
from src.repository.postgres.postgresrepo_client import PostgresRepoClient
from src.requests.client_create import build_create_client_request
from src.responses import ResponseTypes
from src.use_cases.client_create import client_create_use_case
from src.use_cases.token_create import create_token


@pytest.fixture
def client_dict():
    return {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'razao_social': 'New Company',
        'cnpj': '11.111.111/1111-11',
        'email': 'new_company@email.com',
        'dt_inclusao': '01/01/2023 00:00:00',
        'dt_alteracao': '01/01/2023 00:00:00',
        'ativo': True,
    }


def test_create_client_success(client_dict):
    repo = mock.Mock(spec=PostgresRepoClient)

    new_client = {
        'razao_social': 'New Company',
        'cnpj': '11.111.111/1111-11',
        'email': 'new_company@email.com',
    }

    repo.list_client.return_value = []
    repo.create_client.return_value = Client.from_dict(client_dict)

    request = build_create_client_request(new_client)

    result = client_create_use_case(repo, request)

    token = create_token(result.value)

    assert bool(result) is True
    assert isinstance(result.value, Client)
    repo.create_client.assert_called_with(new_client)
    repo.create_token.assert_called_with(token.to_dict())


def test_create_client_already_exists(client_dict):
    repo = mock.Mock()
    repo.list_client.return_value = client_dict

    request = build_create_client_request(client_dict)

    result = client_create_use_case(repo, request)

    assert bool(result) is False
    repo.list_client.assert_called_with(
        filters={'cnpj__eq': request.data['cnpj']}
    )
    assert result.value == {
        'type': ResponseTypes.DOMAIN_ERROR,
        'message': 'O CNPJ já existe',
    }


@pytest.mark.skip('olhar depois')
def test_create_client_handles_generic_error():
    repo = mock.Mock()
    repo.create_client.side_effect = Exception('Just an error message')

    new_client = {
        'razao_social': 'New Company',
        'cnpj': '',
        'email': 'new_company@email.com',
    }

    request = build_create_client_request(new_client)

    result = client_create_use_case(repo, request)

    assert bool(result) is False
    assert result.value == {
        'type': ResponseTypes.SYSTEM_ERROR,
        'message': 'Exception: Just an error message',
    }


def test_create_client_handles_cnjp_validation_error():
    repo = mock.Mock()

    invalid_client_data = {
        'razao_social': 'New Company',
        'cnpj': 'invalid_cnpj_format',
        'email': 'new_company@email.com',
    }

    request = build_create_client_request(invalid_client_data)

    result = client_create_use_case(repo, request)

    assert bool(result) is False
    assert result.value == {
        'type': ResponseTypes.PARAMETERS_ERROR,
        'message': 'value: Invalid CNPJ',
    }


def test_create_client_handles_email_validation_error():
    repo = mock.Mock()

    invalid_client_data = {
        'razao_social': 'New Company',
        'cnpj': '11.111.111/1111-11',
        'email': 'invalid_email_format',
    }

    request = build_create_client_request(invalid_client_data)

    result = client_create_use_case(repo, request)

    assert bool(result) is False
    assert result.value == {
        'type': ResponseTypes.PARAMETERS_ERROR,
        'message': 'value: Invalid e-mail',
    }
