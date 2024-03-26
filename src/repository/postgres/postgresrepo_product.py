# pylint: disable=c0103
# pylint: disable=c0209
# pylint: disable=c0116
from typing import Dict, List

from sqlmodel import select

from src.domain import product
from src.repository.postgres.base_postgresrepo import BasePostgresRepo
from src.repository.postgres.postgres_objects import Category as PgCategory
from src.repository.postgres.postgres_objects import Client as PgClient
from src.repository.postgres.postgres_objects import Product as PgProduct


class PostgresRepoProduct(BasePostgresRepo):
    """Postgres Product repository"""

    def __init__(self) -> None:
        super().__init__()

    def _create_product_objects(self, result: list[PgProduct]):
        return [
            product.Product(
                id=p.id,
                code=p.code,
                nome=p.nome,
                descricao=p.descricao,
                sku=p.sku,
                categoria_id=p.categoria_id,
                dt_inclusao=p.dt_inclusao,
                dt_alteracao=p.dt_alteracao,
                ativo=p.ativo,
            )
            for p in result
        ]

    def list_product(self, filters=None) -> List[product.Product]:
        session = self._create_session()

        query = session.query(PgProduct)

        if filters is not None:
            if 'client_id__eq' in filters:
                client_id = filters['client_id__eq']

                query = (
                    session.query(PgProduct)
                    .join(PgCategory, PgProduct.categoria_id == PgCategory.id)
                    .join(PgClient, PgCategory.client_id == PgClient.id)
                    .filter(PgClient.id == client_id)
                    # .options(joinedload(PgProduct.category).joinedload(PgCategory.client))
                )

            if 'id__eq' in filters:
                query = query.filter(PgProduct.id == filters['id__eq'])

            if 'code__eq' in filters:
                query = query.filter(PgProduct.code == filters['code__eq'])

            if 'ativo__eq' in filters:
                query = query.filter(PgProduct.ativo == filters['ativo__eq'])

            if 'categoria_id__eq' in filters:
                query = query.filter(
                    PgProduct.categoria_id == filters['categoria_id__eq']
                )

            if 'sku__eq' in filters:
                query = query.filter(PgProduct.sku == filters['sku__eq'])

            if 'page__eq' in filters and 'items_per_page__eq' in filters:
                page = int(filters['page__eq'])
                items_per_page = int(filters['items_per_page__eq'])
                query = (
                    query.order_by('id')
                    .limit(items_per_page)
                    .offset((page - 1) * items_per_page)
                )

            if 'nome__in' in filters:
                query = query.filter(PgProduct.nome.in_(filters['nome__in']))

        return self._create_product_objects(query.all())

    def create_product(self, products: list) -> int | None:
        session = self._create_session()

        try:
            session.bulk_insert_mappings(
                PgProduct, [PgProduct(**product) for product in products]
            )
        except:
            session.rollback()
            raise
        else:
            session.commit()
            return len(products)

    def update_product(self, new_product_data: Dict) -> product.Product:
        session = self._create_session()

        try:
            statement = select(PgProduct).where(
                PgProduct.id == new_product_data['id']
            )
            pg_product_obj = session.exec(statement).one()

            for field, value in new_product_data.items():
                setattr(pg_product_obj, field, value)
        except:
            session.rollback()
            raise
        else:
            session.commit()

        return self._create_product_objects([pg_product_obj])[0]
