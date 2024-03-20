import json
import logging
import pickle
import time

from pandas import DataFrame

from src.errors.types import CacheEmptyError
from src.recomendacao.training_pipeline import CACHE_HASH


class ModelManager:
    def __init__(self, repo_db, repo_cache):
        self._models = {}
        self._repo_db = repo_db
        self._repo_cache = repo_cache
        self._models_params = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def load_models_from_cache(self):
        self.logger.info('Loading models from cache...')

        # Fetch models and parameters from database
        self._models_params = self.fetch_params_from_db()
        self.logger.info('Fetched parameters from database.')

        for client_id, algorithm, parameters in self.generate_rows():
            self.logger.info(
                f'Processing client_id: {client_id}, algorithm: {algorithm}'
            )

            if algorithm == 'implicit':
                algo_type = parameters.get('algo_type')
                if algo_type is not None:
                    model_to_search = f'{client_id}-{algo_type}'
            else:
                model_to_search = f'{client_id}-{algorithm}'

            self.logger.info(f'Searching for model: {model_to_search}')

            start_time = time.time()
            model_instance = self.load_model_from_cache(model_to_search)
            end_time = time.time()
            load_duration = end_time - start_time

            self._models[model_to_search] = model_instance

            self.logger.info(
                f'Loaded model: {model_to_search} into memory in {load_duration:.4f} seconds.'
            )

        self.logger.info('Finished loading models from cache.')

    def get_model(self, model_name):
        return self._models[model_name]

    def fetch_params_from_db(self):
        query = """ SELECT
                        algoritmo,
                        params,
                        client_id
                    FROM algoparams
                    WHERE ativo = 1;"""
        with self._repo_db.engine.begin() as connection:
            result = connection.exec_driver_sql(query).fetchall()

        data = [
            (algo, json.loads(params), client_id)
            for algo, params, client_id in result
        ]

        column_names = [
            'algoritmo',
            'params',
            'client_id',
        ]
        return DataFrame(data, columns=column_names)

    def generate_rows(self):
        for _, row in self._models_params.iterrows():
            parameters_dict = row[['params']].to_dict()
            yield row['client_id'], row['algoritmo'], parameters_dict['params']

    def load_model_from_cache(self, model_to_search: str):

        result = self._repo_cache.get_hash(CACHE_HASH, model_to_search)

        if result is None:
            raise CacheEmptyError(
                f'Não foram encontradas informações no cache para {model_to_search}'
            )

        try:
            return pickle.loads(result)
        except Exception:
            return json.loads(result)
