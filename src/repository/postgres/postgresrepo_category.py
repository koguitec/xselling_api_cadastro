# pylint: disable=c0103
# pylint: disable=c0209
# pylint: disable=c0116
from typing import Dict, List

from sqlalchemy import text
from sqlmodel import select

from src.domain import category
from src.repository.postgres.base_postgresrepo import BasePostgresRepo
from src.repository.postgres.postgres_objects import Category as PgCategory


class PostgresRepoCategory(BasePostgresRepo):
    """Postgres Category repository"""

    def __init__(self) -> None:
        super().__init__()

    def _create_category_objects(
        self, result: list[PgCategory]
    ) -> List[category.Category]:
        return [
            category.Category(
                id=c.id,
                code=c.code,
                descricao=c.descricao,
                client_id=c.client_id,
                dt_inclusao=c.dt_inclusao,
                dt_alteracao=c.dt_alteracao,
                ativo=c.ativo,
            )
            for c in result
        ]

    def list_category(self, filters=None) -> List[category.Category]:
        session = self._create_session()

        query = session.query(PgCategory)

        if filters is None:
            return self._create_category_objects(query.all())

        if 'client_id__eq' in filters:
            query = query.filter(
                PgCategory.client_id == filters['client_id__eq']
            )

        if 'id__eq' in filters:
            query = query.filter(PgCategory.id == filters['id__eq'])

        if 'code__eq' in filters:
            query = query.filter(PgCategory.code == filters['code__eq'])

        if 'ativo__eq' in filters:
            query = query.filter(PgCategory.ativo == filters['ativo__eq'])

        if 'client_id__eq' in filters:
            query = query.filter(
                PgCategory.client_id == filters['client_id__eq']
            )

        if 'descricao__eq' in filters:
            query = (
                session.query(PgCategory)
                .filter(text('descricao LIKE :descricao'))
                .params(descricao=f"%{filters['descricao__eq']}%")
            )

        if 'page__eq' in filters and 'items_per_page__eq' in filters:
            page = int(filters['page__eq'])
            items_per_page = int(filters['items_per_page__eq'])
            query = (
                query.order_by('id')
                .limit(items_per_page)
                .offset((page - 1) * items_per_page)
            )

        return self._create_category_objects(query.all())

    def create_category(self, new_category: Dict) -> category.Category:
        session = self._create_session()

        try:
            pg_category_obj = PgCategory(**new_category)
            session.add(pg_category_obj)
        except:
            session.rollback()
            raise
        else:
            session.commit()

        return self._create_category_objects([pg_category_obj])[0]

    def update_category(self, new_category_data: Dict) -> category.Category:
        session = self._create_session()

        try:
            statement = select(PgCategory).where(
                PgCategory.id == new_category_data['id']
            )
            pg_category_obj = session.exec(statement).one()

            for field, value in new_category_data.items():
                setattr(pg_category_obj, field, value)
        except:
            session.rollback()
            raise
        else:
            session.commit()

        return self._create_category_objects([pg_category_obj])[0]
