import json
import pickle
from typing import Any

from pandas import DataFrame

from src.interfaces.recommender import AlgorithmStrategyInterface
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.postgres.base_postgresrepo import BasePostgresRepo

from ..recomendacao.training_pipeline import CACHE_HASH, MODEL_ALS


class ConcreteStrategyImplicit(AlgorithmStrategyInterface):
    def __init__(
        self,
        algorithm: AlgorithmStrategyInterface,
        repo_cache: RedisRepository,
        repo_db: BasePostgresRepo,
        client_id: int,
        params: dict,
    ):
        self._algorithm = algorithm
        self._repo_cache = repo_cache
        self._repo_db = repo_db.engine
        self._client_id = client_id
        self._params = params

    def execute(self, raw_training_data: DataFrame):
        trainig_data = self._format_trainig_data(raw_training_data)

        model, item_to_index = self._train_algorithm(trainig_data)

        self._save_model_to_database()

        self._save_to_cache(model, MODEL_ALS)

        self._save_to_cache(item_to_index, 'item_to_index')

    def _format_trainig_data(self, raw_training_data: DataFrame):
        raw_training_data['categorias'] = raw_training_data[
            'categorias'
        ].apply(lambda x: json.loads(x))
        return raw_training_data

    def _train_algorithm(self, training_data):
        self._algorithm.set_parameters(training_data=training_data)
        return self._algorithm.execute()

    def _save_model_to_database(self):
        ...
        # TODO

    def _save_to_cache(self, object_: Any, field_name: str):
        self._repo_cache.insert_hash(
            key=CACHE_HASH,
            field=f'{self._client_id}-{field_name}',
            value=pickle.dumps(object_),
        )
