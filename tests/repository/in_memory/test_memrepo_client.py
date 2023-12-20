"""Test module for client list use case"""
# pylint: disable=w0621
# pylint: disable=c0116
import pytest

from src.domain.client import Client
from src.repository.in_memory.memrepo_client import MemRepo


@pytest.fixture
def clients_dicts():
    return [
        {
            'id': 1,
            'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
            'razao_social': 'My company 1',
            'cnpj': '00.000.000/0000-01',
            'email': 'mycompany_1@email.com',
            'dt_inclusao': '01/01/2023 00:00:0',
            'dt_alteracao': None,
            'ativo': True,
        },
        {
            'id': 2,
            'code': 'fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
            'razao_social': 'My company 2',
            'cnpj': '00.000.000/0000-02',
            'email': 'mycompany_2@email.com',
            'dt_inclusao': '01/01/2023 00:00:0',
            'dt_alteracao': None,
            'ativo': True,
        },
        {
            'id': 3,
            'code': '913694c6-435a-4366-ba0d-da5334a611b2',
            'razao_social': 'My company 3',
            'cnpj': '00.000.000/0000-03',
            'email': 'mycompany_3@email.com',
            'dt_inclusao': '01/01/2023 00:00:0',
            'dt_alteracao': None,
            'ativo': False,
        },
        {
            'id': 4,
            'code': 'eed76e77-55c1-41ce-985d-ca49bf6c0585',
            'razao_social': 'My company 4',
            'cnpj': '00.000.000/0000-04',
            'email': 'mycompany_4@email.com',
            'dt_inclusao': '01/01/2023 00:00:0',
            'dt_alteracao': None,
            'ativo': False,
        },
    ]


def test_client_repository_list_without_parameters(clients_dicts):
    repo = MemRepo(clients_dicts)

    clients = [Client.from_dict(c) for c in clients_dicts]

    assert repo.list_client() == clients


def test_client_repository_list_with_code_equal_filter(clients_dicts):
    repo = MemRepo(clients_dicts)

    clients = repo.list_client(
        {'code__eq': 'f853578c-fc0f-4e65-81b8-566c5dffa35a'}
    )

    assert len(clients) == 1
    assert clients[0].code == 'f853578c-fc0f-4e65-81b8-566c5dffa35a'


def test_client_repository_list_with_ativo_equal_true_filter(clients_dicts):
    repo = MemRepo(clients_dicts)

    clients = repo.list_client({'ativo__eq': 'true'})

    assert len(clients) == 2
    assert set([c.code for c in clients]) == {
        'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
    }


def test_client_repository_list_with_ativo_equal_false_filter(clients_dicts):
    repo = MemRepo(clients_dicts)

    clients = repo.list_client({'ativo__eq': False})

    assert len(clients) == 2
    assert set([c.code for c in clients]) == {
        '913694c6-435a-4366-ba0d-da5334a611b2',
        'eed76e77-55c1-41ce-985d-ca49bf6c0585',
    }


def test_client_repository_create(clients_dicts):
    repo = MemRepo(clients_dicts)

    new_client = {
        'razao_social': 'My company 5',
        'cnpj': '00.000.000/0000-05',
        'email': 'mycompany_4@email.com',
        'ativo': True,
    }

    repo.create_client(new_client)

    assert len(clients_dicts) == 5


def test_client_repository_get_client_by_code(clients_dicts):
    repo = MemRepo(clients_dicts)
    client = repo.get_client_by_code('fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a')

    assert client['code'] == 'fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a'


def test_client_repository_update_client(clients_dicts):
    repo = MemRepo(clients_dicts)

    new_client_data = {
        'code': 'eed76e77-55c1-41ce-985d-ca49bf6c0585',
        'razao_social': 'My company 4',
        'cnpj': '00.000.000/0000-04',
        'email': 'mycompany_4@email.com',
        'ativo': True,
    }

    repo.update_client(new_client_data)

    updated_client = {}
    for client in clients_dicts:
        if client['code'] == 'eed76e77-55c1-41ce-985d-ca49bf6c0585':
            updated_client = client

    assert len(clients_dicts) == 4
    assert updated_client['ativo'] is True
