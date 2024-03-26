import json

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.postgres.base_postgresrepo import BasePostgresRepo

CLIENT_ITEM_INFO_HASH = 'cross_selling_sku_to_item_info_client_id_'
CLIENT_CAT_TO_ITEM_MAPPER = 'cross_selling_cat_id_to_item_client_id_'


class CacheService:
    def __init__(self) -> None:
        self._repo_db = BasePostgresRepo()
        self._repo_cache = RedisRepository()

    def load_client_items(self, client_id: str) -> None:
        """Full load of client's items from database to cache store.
        The data is a dictionary containg info of client's items with the item
        sku as the dictionary key.

        Example:
        ...
        'AM7008': {
            'descricao': 'AGULHA CANETA DE INSULINA',
            'id': 224,
            'nome': 'AGULHA CANETA INSUL 31G 5MM (JH)'
            },
        'AM7009': {
            'descricao': 'AGULHA CANETA DE INSULINA',
            'id': 224,
            'nome': 'AGULHA CANETA INSUL 30G 8MM (JH)'
            },
        ...

        Args:
            client_id (str): Client's ID

        return:
            None
        """

        # Optimized SQL query that retrieves only the necessary columns
        query = """
                SELECT p.sku, c.id as categoria_id, c.descricao, p.nome
                FROM category c
                        JOIN product p ON c.id = p.categoria_id
                WHERE c.client_id = :client_id AND c.ativo = 1 AND p.ativo = 1;
                """

        # Execute query and directly load into a hashtable format
        sku_to_item = {}
        with Session(self._repo_db.engine) as session:
            session.bulk
            result = session.execute(
                text(query), {'client_id': client_id}
            ).all()
            for sku, id, descricao, nome in result:
                sku_to_item[sku] = {
                    'id': id,
                    'descricao': descricao,
                    'nome': nome,
                }

        # Pipeline Redis insertions
        pipeline = self._repo_cache.pipeline()
        hash_name = CLIENT_ITEM_INFO_HASH + client_id
        for sku, item in sku_to_item.items():
            pipeline.hset(hash_name, sku, json.dumps(item))
        pipeline.execute()

    def load_client_mapper_cat_to_items(
        self, client_id: str, items: list = None
    ) -> None:
        query = """
                SELECT
                    c.id as id_categoria,
                    p.nome,
                    p.descricao as descricao_produto,
                    c.descricao as descricao_categoria,
                    p.sku,
                    p.categoria_id
                FROM category c 
                INNER JOIN product p ON c.id = p.categoria_id
                WHERE c.client_id = :client_id AND p.Ativo = 1
                """

        if items is not None:
            new_items_list: list = [product['sku'] for product in items]
            query += f'AND p.sku in {tuple(new_items_list) if len(new_items_list) > 1 else (new_items_list[0], new_items_list[0])}'

        with Session(self._repo_db.engine) as session:
            result = session.execute(
                text(query), {'client_id': client_id}
            ).all()

        # Transform the rows into a dictionary grouped by 'id_categoria'
        cat_id_to_prods = {}
        for row in result:
            # Deconstruct the row into columns.
            (
                id_categoria,
                nome,
                descricao_produto,
                descricao_categoria,
                sku,
                categoria_id,
            ) = row

            # Create the product record excluding the id_categoria as it's used for grouping.
            product_record = {
                'nome': nome,
                'descricao_produto': descricao_produto,
                'descricao_categoria': descricao_categoria,
                'sku': sku,
                'categoria_id': categoria_id,
            }

            # Add the product record to the appropriate list in the dictionary.
            if id_categoria not in cat_id_to_prods:
                cat_id_to_prods[id_categoria] = []
            cat_id_to_prods[id_categoria].append(product_record)

        # Pipeline Redis insertions
        pipeline = self._repo_cache.pipeline()
        hash_name = CLIENT_CAT_TO_ITEM_MAPPER + str(client_id)
        for cat, items in cat_id_to_prods.items():
            pipeline.hset(hash_name, cat, json.dumps(items))
        pipeline.execute()

    def update_client_items_in_cache(
        self, client_id: str, items: list
    ) -> None:

        # Update items per category in cache
        self.load_client_mapper_cat_to_items(client_id=client_id, items=items)

        # Pipeline Redis insertions
        pipeline = self._repo_cache.pipeline()
        hash_name = CLIENT_ITEM_INFO_HASH + str(client_id)
        for product in items:
            sku = product.pop('sku')
            pipeline.hset(hash_name, sku, json.dumps(product))
        pipeline.execute()
