"""Test module for the Client entity"""
# pylint: disable=c0116
from src.domain.client import Client


def test_client_model_init():
    client = Client(
        razao_social='My company',
        cnpj='00.000.000/0000-00',
        email='mycompany@email.com',
    )

    assert client.id is None
    assert client.code is None
    assert client.razao_social == 'My company'
    assert client.cnpj == '00.000.000/0000-00'
    assert client.email == 'mycompany@email.com'
    assert client.dt_inclusao is None
    assert client.dt_alteracao is None
    assert client.ativo is True


def test_client_model_init_with_defaults():
    client = Client(
        id=1,
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        razao_social='My company',
        cnpj='00.000.000/0000-00',
        email='mycompany@email.com',
        dt_inclusao='01/01/2023, 00:00:00',
        dt_alteracao='01/01/2023, 00:00:00',
        ativo=True,
    )

    assert client.id == 1
    assert client.code == 'f853578c-fc0f-4e65-81b8-566c5dffa35a'
    assert client.razao_social == 'My company'
    assert client.cnpj == '00.000.000/0000-00'
    assert client.email == 'mycompany@email.com'
    assert client.dt_inclusao == '01/01/2023, 00:00:00'
    assert client.dt_alteracao == '01/01/2023, 00:00:00'
    assert client.ativo is True


def test_client_model_from_dict():
    init_dict = {
        'razao_social': 'My company',
        'cnpj': '00.000.000/0000-00',
        'email': 'mycompany@email.com',
    }

    client = Client.from_dict(init_dict)

    assert client.id is None
    assert client.code is None
    assert client.razao_social == 'My company'
    assert client.cnpj == '00.000.000/0000-00'
    assert client.email == 'mycompany@email.com'
    assert client.dt_inclusao is None
    assert client.dt_alteracao is None
    assert client.ativo is True


def test_client_model_to_dict():
    init_dict = {
        'id': 1,
        'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
        'razao_social': 'My company',
        'cnpj': '00.000.000/0000-00',
        'email': 'mycompany@email.com',
        'dt_inclusao': '01/01/2023, 00:00:00',
        'dt_alteracao': '01/01/2023, 00:00:00',
        'ativo': True,
    }

    client = Client.from_dict(init_dict)

    assert client.to_dict() == init_dict


def test_client_model_comparison():
    init_dict = {
        'razao_social': 'My company',
        'cnpj': '00.000.000/0000-00',
        'email': 'mycompany@email.com',
    }

    client1 = Client.from_dict(init_dict)
    client2 = Client.from_dict(init_dict)

    assert client1 == client2
