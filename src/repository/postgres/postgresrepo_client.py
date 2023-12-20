"""Module for Postgres repository"""
# pylint: disable=c0103
# pylint: disable=c0209
# pylint: disable=c0116
from typing import Dict, List

from sqlmodel import select

from src.domain import auth_jwt, client
from src.repository.postgres.base_postgresrepo import BasePostgresRepo
from src.repository.postgres.postgres_objects import AuthJwt as PgAuthJwt
from src.repository.postgres.postgres_objects import Client as PgClient


class PostgresRepoClient(BasePostgresRepo):
    """Postgres Client repository"""

    def __init__(self) -> None:
        super().__init__()

    def _create_client_objects(
        self, results: list[PgClient]
    ) -> List[client.Client]:
        return [
            client.Client(
                id=c.id,
                code=c.code,
                cnpj=c.cnpj,
                email=c.email,
                razao_social=c.razao_social,
                dt_inclusao=c.dt_inclusao,
                dt_alteracao=c.dt_alteracao,
                ativo=c.ativo,
            )
            for c in results
        ]

    def _create_token_objects(self, t: PgAuthJwt) -> auth_jwt.AuthJwt:
        return auth_jwt.AuthJwt(
            id=t.id,
            jti=t.jti,
            client_id=t.client_id,
            token_type=t.token_type,
            revoked=t.revoked,
            expires=t.expires,
        )

    def list_client(self, filters=None) -> List[client.Client]:
        session = self._create_session()

        query = session.query(PgClient)

        if filters is None:
            return self._create_client_objects(query.all())

        if 'id__eq' in filters:
            query = query.filter(PgClient.id == filters['id__eq'])

        if 'code__eq' in filters:
            query = query.filter(PgClient.code == filters['code__eq'])

        if 'ativo__eq' in filters:
            query = query.filter(PgClient.ativo == filters['ativo__eq'])

        if 'cnpj__eq' in filters:
            query = query.filter(PgClient.cnpj == filters['cnpj__eq'])

        return self._create_client_objects(query.all())

    def create_client(self, new_client: client.Client) -> client.Client:
        session = self._create_session()

        try:
            pg_client_obj = PgClient(**new_client.to_dict())
            session.add(pg_client_obj)
        except:
            session.rollback()
            raise
        else:
            session.commit()

        return self._create_client_objects([pg_client_obj])[0]

    def update_client(self, new_client_data: Dict) -> client.Client:
        session = self._create_session()

        try:
            statement = select(PgClient).where(
                PgClient.id == new_client_data['id']
            )
            pg_client_obj = session.exec(statement).one()

            for field, value in new_client_data.items():
                setattr(pg_client_obj, field, value)
        except:
            session.rollback()
            raise
        else:
            session.commit()

        return self._create_client_objects([pg_client_obj])[0]

    def create_token(self, new_token: dict) -> auth_jwt.AuthJwt:
        session = self._create_session()

        try:
            pg_token_obj = PgAuthJwt(**new_token)
            session.add(pg_token_obj)
        except:
            session.rollback()
            raise
        else:
            session.commit()

        return self._create_token_objects(pg_token_obj)
