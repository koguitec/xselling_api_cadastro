import json
import pickle

import numpy as np

from main import global_model_manager
from src.errors.types import CacheEmptyError
from src.interfaces.recommender import AlgorithmStrategyInterface
from src.recomendacao.training_pipeline import CACHE_HASH, MODEL_ALS
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.postgres.postgresrepo_product import PostgresRepoProduct


class ImplicitRecommenderList(AlgorithmStrategyInterface):
    def __init__(self):
        self._repo_cache = RedisRepository()
        self._repo_db = PostgresRepoProduct()

    def execute(self, items_sku: list, client_id: str):

        category_names: list[str] = self._search_items_on_cache(items_sku)

        item_to_index: dict = self._search_on_cache(client_id, 'item_to_index')

        selected_items: list[int] = self._filter_selected_items(
            item_to_index, category_names
        )

        model = global_model_manager.get_model(f'{client_id}-{MODEL_ALS}')

        ids, scores = model.similar_items(*selected_items)

        return self._format_output(item_to_index, ids, scores)

    def _search_items_on_cache(self, items_sku: list):
        sku_to_item = self._repo_cache.get_hash(CACHE_HASH, 'sku_to_item')

        if sku_to_item is None:
            raise CacheEmptyError('Mapper sku_to_item não encontrado no cache')

        sku_to_item = json.loads(sku_to_item)

        return [
            sku_to_item[key]['descricao']
            for key in items_sku
            if key in sku_to_item
        ]

    def _search_on_cache(self, client_id, field_name: str):

        result = self._repo_cache.get_hash(
            CACHE_HASH, f'{client_id}-{field_name}'
        )

        if result is None:
            raise CacheEmptyError(
                f'Não foram encontradas informações no cache para {field_name}'
            )

        return pickle.loads(result)

    def _filter_selected_items(
        self, item_to_index, category_names
    ) -> list[str]:
        return [
            index
            for item, index in item_to_index.items()
            if item in category_names
        ]

    def _format_output(self, item_to_index, ids, scores) -> dict:

        item_to_score = {
            item: round(float(score), 2)
            for item, score in zip(
                np.array(list(item_to_index.keys()))[ids], scores
            )
        }

        cat_id_to_prods = self._repo_cache.get_hash(
            CACHE_HASH, 'cat_id_to_items'
        )

        if cat_id_to_prods is None:
            raise CacheEmptyError(
                'Mapper cat_id_to_items não encontrado no cache'
            )

        cat_id_to_prods = json.loads(cat_id_to_prods)

        descriptors_to_match = list(np.array(list(item_to_index.keys()))[ids])

        recommender = [
            item
            for sublist in cat_id_to_prods.values()
            for item in sublist
            if item['descricao_categoria'] in descriptors_to_match
        ]

        # Adding the 'score' key to each dictionary by matching 'descricao_categoria'
        # with the key of item_to_score
        for item in recommender:
            item['score'] = item_to_score.get(
                item['descricao_categoria'], None
            )

        sorted_recommender = sorted(
            recommender, key=lambda x: x.get('score', 0), reverse=True
        )

        return {
            'type': 'Recomendacao - ALS',
            'count': len(sorted_recommender),
            'attributes': sorted_recommender,
        }
