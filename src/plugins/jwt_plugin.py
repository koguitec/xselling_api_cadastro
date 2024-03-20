from datetime import datetime, timedelta

import jwt

from application.rest.adapters.request_adapter import HttpRequest
from src.errors.types.token_expired_error import ExpiredTokenError
from src.errors.types.token_invalid_error import TokenInvalidError


class AuthTokenPlugin:
    SECRET = '1234'
    ALGORITHM = 'HS256'
    EXPIRES = datetime.now() + timedelta(days=365)

    def __init__(self, jwt: jwt) -> None:
        self.jwt = jwt

    def create_jwt(self, data: dict) -> list[str, datetime]:
        expire_date = self.EXPIRES
        data.update({'exp': expire_date})
        return (
            self.jwt.encode(data, self.SECRET, algorithm=self.ALGORITHM),
            expire_date,
        )

    def decode_jwt(self, data: str) -> dict:
        return self.jwt.decode(data, self.SECRET, self.ALGORITHM)

    def validate_token(self, http_request: HttpRequest):
        try:
            token = http_request.headers
            return self.decode_jwt(token['Authorization'])
        except self.jwt.ExpiredSignatureError:
            raise ExpiredTokenError('Token expirado')
        except self.jwt.InvalidTokenError:
            raise TokenInvalidError('Token inválido')


auth_token = AuthTokenPlugin(jwt)
