from datetime import datetime, timedelta

import jwt


class AuthTokenPlugin:
    SECRET = '1234'
    ALGORITHM = 'HS256'
    EXPIRES = datetime.now() + timedelta(days=365)

    def __init__(self, jwt: jwt) -> None:
        self.jwt = jwt

    def create_jwt(self, data: dict) -> [str, datetime]:
        expire_date = self.EXPIRES
        data.update({'exp': expire_date})
        return (
            self.jwt.encode(data, self.SECRET, algorithm=self.ALGORITHM),
            expire_date,
        )

    def decode_jwt(self, data: str) -> dict:
        return self.jwt.decode(data, self.SECRET, self.ALGORITHM)


auth_token = AuthTokenPlugin(jwt)
