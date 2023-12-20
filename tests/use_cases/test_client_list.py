"""Test module for client list use cases"""
# pylint: disable=w0621
from unittest import mock

import pytest

from src.domain.client import Client
from src.requests.client_list import build_client_list_request
from src.responses import ResponseTypes
from src.use_cases.client_list import client_list_use_case


@pytest.fixture
def domain_clients():
    client_1 = Client(
        id=1,
        code='0000-0000-0000-0000-0000-0000',
        razao_social='My company 1',
        cnpj='00.000.000/0000-01',
        email='mycompany_1@email.com',
        dt_inclusao='01/01/2023 00:00:00',
        dt_alteracao='01/01/2023 00:00:00',
        ativo=True,
    )
    client_2 = Client(
        id=2,
        code='0000-0000-0000-0000-0000-0000',
        razao_social='My company 2',
        cnpj='00.000.000/0000-02',
        email='mycompany_1@email.com',
        dt_inclusao='01/01/2023 00:00:00',
        dt_alteracao='01/01/2023 00:00:00',
        ativo=True,
    )
    client_3 = Client(
        id=3,
        code='0000-0000-0000-0000-0000-0000',
        razao_social='My company 3',
        cnpj='00.000.000/0000-03',
        email='mycompany_1@email.com',
        dt_inclusao='01/01/2023 00:00:00',
        dt_alteracao='01/01/2023 00:00:00',
        ativo=False,
    )
    client_4 = Client(
        id=4,
        code='0000-0000-0000-0000-0000-0000',
        razao_social='My company 4',
        cnpj='00.000.000/0000-04',
        email='mycompany_1@email.com',
        dt_inclusao='01/01/2023 00:00:00',
        dt_alteracao='01/01/2023 00:00:00',
        ativo=False,
    )

    return [client_1, client_2, client_3, client_4]


def test_client_list_without_parameters(domain_clients):
    repo = mock.Mock()
    repo.list_client.return_value = domain_clients

    request = build_client_list_request()

    response = client_list_use_case(repo, request)

    assert bool(response) is True
    repo.list_client.assert_called_with(filters=None)
    assert response.value == domain_clients


def test_client_list_with_id_equal_filters(domain_clients):
    repo = mock.Mock()
    repo.list_client.return_value = domain_clients

    qry_filters = {'id__eq': 1}
    request = build_client_list_request(filters=qry_filters)

    response = client_list_use_case(repo, request)

    assert bool(response) is True
    repo.list_client.assert_called_with(filters=qry_filters)
    assert response.value == domain_clients


def test_client_list_handles_generic_error():
    repo = mock.Mock()
    repo.list_client.side_effect = Exception('Just an error message')

    request = build_client_list_request(filters={})

    response = client_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.SYSTEM_ERROR,
        'message': 'Exception: Just an error message',
    }


def test_client_list_handles_bad_request():
    repo = mock.Mock()

    request = build_client_list_request(filters=5)

    response = client_list_use_case(repo, request)

    assert bool(response) is False
    assert response.value == {
        'type': ResponseTypes.PARAMETERS_ERROR,
        'message': 'filters: Is not iterable',
    }
