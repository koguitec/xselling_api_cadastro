"""Test module for Client serializer"""
import json

from src.domain.auth_jwt import AuthJwt
from src.serializers.auth_jwt import ClientAuthJsonEncoder


def test_serialize_domain_client():
    auth = AuthJwt(
        id=1,
        client_id=1,
        jti='test',
        token_type='refresh',
        revoked=False,
        expires=None,
    )

    excepted_json = """
        {
            "id": 1,
            "client_id": 1,
            "jti": "test",
            "token_type": "refresh",
            "revoked": false,
            "expires": null
        }
        """

    json_auth = json.dumps(auth, cls=ClientAuthJsonEncoder)

    assert json.loads(json_auth) == json.loads(excepted_json)
