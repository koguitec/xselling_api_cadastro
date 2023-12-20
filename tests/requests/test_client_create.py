import uuid

from src.requests.client_create import build_create_client_request


def test_build_client_create_request():
    new_client = {
        'razao_social': 'My company',
        'cnpj': '00.000.000/0000-00',
        'email': 'mycompany@email.com',
    }
    request = build_create_client_request(new_client)

    assert bool(request) is True
    assert 'code' in new_client
    assert isinstance(new_client['code'], uuid.UUID)
