from src.domain.auth_jwt import AuthJwt, TokenTypeEnum
from src.domain.client import Client
from src.plugins.jwt_plugin import auth_token


def create_token(client: Client) -> None:
    client_id = client.id
    cnpj = client.cnpj

    token, expire_date = auth_token.create_jwt(
        data={'client_id': client_id, 'cnpj': cnpj}
    )

    return AuthJwt(
        jti=token,
        client_id=client_id,
        token_type=TokenTypeEnum.REFRESH.value,
        expires=expire_date,
    )
