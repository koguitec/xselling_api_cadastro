import json

from pandas import DataFrame, read_sql

from src.interfaces.recommender import AlgorithmStrategyInterface
from src.repository.postgres.base_postgresrepo import BasePostgresRepo

from .query.queries import Query

CACHE_HASH = 'cross_selling'
MODEL_APRIORI = 'apriori'
MODEL_ALS = 'als'


class TrainingPipeline:
    def __init__(
        self,
        strategy: AlgorithmStrategyInterface,
        algorithm: str,
        repo_db: BasePostgresRepo,
        params: dict,
        client_id: int,
    ) -> None:
        self._strategy = strategy
        self._conn = repo_db
        self._algorithm = algorithm
        self._params = params
        self._client_id = client_id
        self._query = Query()

    def execute(self):
        raw_training_data = self._fetch_data_on_database()

        self._strategy.execute(raw_training_data)

        self._save_training_pipeline_params_on_database()

    def _fetch_data_on_database(self) -> DataFrame:
        return read_sql(
            sql=self._query.query_dados_treino(self._client_id),
            con=self._conn.engine,
        )

    def _save_training_pipeline_params_on_database(self):

        with self._conn.engine.begin() as connection:
            # Salva parâmetros de configuração do algoritmo no histórico
            connection.exec_driver_sql(
                self._query.save_params_on_data_base(
                    algorithm=self._algorithm,
                    params=json.dumps(self._params),
                    client_id=self._client_id,
                )
            )
