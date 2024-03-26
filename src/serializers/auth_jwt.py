"""Module for the AuthJwt serializer"""
import json


class ClientAuthJsonEncoder(json.JSONEncoder):
    """Serializer class for the client model

    Args:
        json (object): JSONEncoder

    Returns:
        str: serialized object
    """

    def default(self, o):
        try:
            to_serialize = {
                'id': o.id,
                'client_id': o.client_id,
                'jti': o.jti,
                'token_type': o.token_type,
                'revoked': o.revoked,
                'expires': str(o.expires),
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
