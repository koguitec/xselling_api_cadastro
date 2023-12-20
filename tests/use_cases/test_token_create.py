from datetime import datetime

import pytest

from src.domain.auth_jwt import AuthJwt, TokenTypeEnum
from src.domain.client import Client
from src.plugins.jwt_plugin import auth_token
from src.use_cases.token_create import create_token


@pytest.fixture
def client_entity():
    return Client(
        id=1,
        razao_social='My company',
        cnpj='00.000.000/0000-00',
        email='mycompany@email.com',
    )


def test_token_create(client_entity):
    token: AuthJwt = create_token(client_entity)

    assert token.id is None
    assert isinstance(token.expires, datetime)
    assert isinstance(token.jti, str)
    assert token.revoked is False
    assert token.client_id == 1
    assert token.token_type == TokenTypeEnum.REFRESH.value


def test_encode_decode_token(client_entity):
    token, expire_date = auth_token.create_jwt(
        data={'client_id': client_entity.id}
    )

    result = auth_token.decode_jwt(token)

    assert result['client_id'] == 1


def test_token_is_invalid(client_entity):
    auth_token.EXPIRES = datetime.now()

    token, expire_date = auth_token.create_jwt(
        data={'client_id': client_entity.id}
    )
    with pytest.raises(auth_token.jwt.ExpiredSignatureError):
        auth_token.decode_jwt(token)


def test_invalid_client_entity():
    with pytest.raises(Exception):
        create_token(None)
