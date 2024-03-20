import json

from pandas import DataFrame

from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.postgres.base_postgresrepo import BasePostgresRepo


class CacheService:
    @staticmethod
    def update_client_items(client_id: str) -> None:
        repo = BasePostgresRepo()
        repo_cache = RedisRepository()
        query = f"""SELECT
                        p.sku, c.id, c.descricao, p.nome
                    FROM category c
                    INNER JOIN product p
                    ON c.id = p.categoria_id
                    WHERE c.client_id = {client_id}
                    AND c.ativo = 1
                    AND p.ativo = 1;"""

        with repo.engine.begin() as connection:
            result = connection.exec_driver_sql(query).fetchall()
            df = DataFrame(result)
        sku_to_prod = (
            df.groupby('sku', group_keys=False)
            .apply(
                lambda group: group.drop('sku', axis=1).to_dict(
                    orient='records'
                )[0]
            )
            .to_dict()
        )
        repo_cache.insert_hash(
            'cross_selling',
            f'{client_id}_sku_to_item',
            json.dumps(sku_to_prod),
        )

    def update_client_cat_to_items(client_id: str) -> None:
        repo = BasePostgresRepo()
        repo_cache = RedisRepository()
        query = f"""SELECT
                    c.id as id_categoria,
                    p.nome,
                    p.descricao as descricao_produto,
                    c.descricao as descricao_categoria,
                    p.sku,
                    categoria_id
                FROM category c 
                INNER JOIN product p 
                ON c.id = p.categoria_id
                AND p.Ativo = 1
                WHERE c.client_id = {client_id};"""

        with repo.engine.begin() as connection:
            result = connection.exec_driver_sql(query).fetchall()
            df = DataFrame(result)

        cat_id_to_prods = (
            df.groupby('id_categoria')
            .apply(
                lambda group: group.drop('id_categoria', axis=1).to_dict(
                    orient='records'
                )
            )
            .to_dict()
        )
        repo_cache.insert_hash(
            'cross_selling',
            f'{client_id}_cat_id_to_item',
            json.dumps(cat_id_to_prods),
        )
