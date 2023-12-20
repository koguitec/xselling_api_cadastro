from datetime import datetime

from src.domain.auth_jwt import AuthJwt


def test_authjwt_model_init():
    expires = datetime.now()
    jwt = AuthJwt(
        id=1,
        jti='15653932-350d-4020-9463-789fb895e4ad',
        token_type='refresh',
        client_id=1,
        revoked=False,
        expires=expires,
    )

    assert jwt.id == 1
    assert jwt.jti == '15653932-350d-4020-9463-789fb895e4ad'
    assert jwt.token_type == 'refresh'
    assert jwt.client_id == 1
    assert jwt.revoked is False
    assert isinstance(jwt.expires, datetime)


def test_authjwt_model_from_dict():
    expires = datetime.now()
    init_dict = {
        'id': 1,
        'jti': '15653932-350d-4020-9463-789fb895e4ad',
        'token_type': 'refresh',
        'client_id': 1,
        'revoked': False,
        'expires': expires,
    }

    jwt = AuthJwt.from_dict(init_dict)

    assert jwt.id == 1
    assert jwt.jti == '15653932-350d-4020-9463-789fb895e4ad'
    assert jwt.token_type == 'refresh'
    assert jwt.client_id == 1
    assert jwt.revoked is False
    assert isinstance(jwt.expires, datetime)


def test_authjwt_model_to_dict():
    expires = datetime.now()
    init_dict = {
        'id': 1,
        'jti': '15653932-350d-4020-9463-789fb895e4ad',
        'token_type': 'refresh',
        'client_id': 1,
        'revoked': False,
        'expires': expires,
    }

    jwt = AuthJwt.from_dict(init_dict)

    assert jwt.to_dict() == init_dict
