import json

from pandas import DataFrame

from src.interfaces.recommender import AlgorithmStrategyInterface
from src.recomendacao.query.queries import Query
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.postgres.base_postgresrepo import BasePostgresRepo

from ..recomendacao.training_pipeline import CACHE_HASH, MODEL_APRIORI


class ConcreteStrategyApriori(AlgorithmStrategyInterface):
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
        self._query = Query()
        self._client_id = client_id
        self._params = params

    def execute(self, raw_training_data: DataFrame):
        dados_para_treino_formatados: list[
            list
        ] = self._formata_dataframe_treinamento(raw_training_data)
        regras_associacao: DataFrame = self._executa_algoritmo_de_recomendacao(
            dados_para_treino_formatados
        )
        (
            regras_associacao,
            regras_antecedentes,
            regras_consequentes,
        ) = self._formata_dataframe_output_treinamento(
            regras_associacao=regras_associacao
        )

        self._salva_output_treinamento_no_banco(
            regras_associacao=regras_associacao,
            regras_antecedentes_temp=regras_antecedentes,
            regras_consequentes_temp=regras_consequentes,
        )
        self._salva_output_treinamento_no_cache()

    def _formata_dataframe_treinamento(
        self, raw_training_data: DataFrame
    ) -> list[list]:
        return (
            raw_training_data['categorias']
            .apply(lambda x: json.loads(x))
            .tolist()
        )

    def _executa_algoritmo_de_recomendacao(
        self, trainig_data: list[list]
    ) -> DataFrame:
        self._algorithm.set_parameters(training_data=trainig_data)
        return self._algorithm.execute()

    def _formata_dataframe_output_treinamento(
        self, regras_associacao: DataFrame
    ) -> DataFrame:
        regras_associacao['antecedentes_list'] = regras_associacao[
            'antecedents'
        ].apply(lambda x: list(x))
        regras_associacao['consequentes_list'] = regras_associacao[
            'consequents'
        ].apply(lambda x: list(x))

        regras_associacao['antecedents'] = regras_associacao[
            'antecedents'
        ].apply(self._format_list_to_string)
        regras_associacao['consequents'] = regras_associacao[
            'consequents'
        ].apply(self._format_list_to_string)

        regras_associacao['descricao_regra'] = regras_associacao.apply(
            self._create_rule_column, axis=1
        )

        regras_consequentes = DataFrame(
            regras_associacao.drop(
                columns=[
                    'antecedent support',
                    'consequent support',
                    'leverage',
                    'conviction',
                    'zhangs_metric',
                    'antecedents',
                    'consequents',
                    'support',
                    'confidence',
                    'lift',
                    'antecedentes_list',
                ]
            )
            .explode('consequentes_list')
            .to_dict('records')
        )
        regras_antecedentes = DataFrame(
            regras_associacao.drop(
                columns=[
                    'antecedent support',
                    'consequent support',
                    'leverage',
                    'conviction',
                    'zhangs_metric',
                    'antecedents',
                    'consequents',
                    'support',
                    'confidence',
                    'lift',
                    'consequentes_list',
                ]
            )
            .explode('antecedentes_list')
            .to_dict('records')
        )

        regras_associacao['confidence'] = regras_associacao[
            'confidence'
        ].apply(self._format_percentage)
        regras_associacao['support'] = regras_associacao['support'].apply(
            self._format_percentage
        )
        regras_associacao['lift'] = regras_associacao['lift'].apply(
            self._format_decimal
        )

        regras_associacao['ativo'] = True
        regras_associacao['client_id'] = self._client_id

        regras_associacao.rename(
            columns={
                'confidence': 'confianca',
                'support': 'suporte',
                'antecedents': 'antecedentes',
                'consequents': 'consequentes',
                'lift': 'lift',
            },
            inplace=True,
        )

        columns_to_drop = [
            'antecedentes',
            'consequentes',
            'antecedent support',
            'consequent support',
            'leverage',
            'conviction',
            'zhangs_metric',
        ]

        regras_associacao.drop(columns=columns_to_drop, inplace=True)

        ordem_colunas = [
            'descricao_regra',
            'confianca',
            'suporte',
            'lift',
            'ativo',
            'client_id',
        ]
        regras_associacao = regras_associacao[ordem_colunas]

        return regras_associacao, regras_antecedentes, regras_consequentes

    def _salva_output_treinamento_no_banco(
        self,
        *,
        regras_associacao: DataFrame,
        regras_antecedentes_temp: DataFrame,
        regras_consequentes_temp: DataFrame,
    ) -> None:
        with self._repo_db.begin() as connection:
            # Deleta regras antigas do cliente antes da atualização
            connection.exec_driver_sql(
                self._query.delete_regras_associacao_old(self._client_id)
            )

            regras_associacao.to_sql(
                name='regra',
                con=connection,
                index=False,
                method=None,
                if_exists='append',
            )

            connection.exec_driver_sql(self._query.cria_tabelas_temporarias())

            regras_antecedentes_temp.to_sql(
                name='tempantecedente',
                con=connection,
                index=False,
                method=None,
                if_exists='replace',
            )
            regras_consequentes_temp.to_sql(
                name='tempconsequente',
                con=connection,
                index=False,
                method=None,
                if_exists='replace',
            )

            connection.exec_driver_sql(
                self._query.atualiza_tabela_regra_categoria()
            )

            connection.exec_driver_sql(
                self._query.remove_tabelas_temporarias()
            )

        self._repo_db.dispose()

    def _salva_output_treinamento_no_cache(self) -> None:
        with self._repo_db.begin() as connection:
            result = connection.exec_driver_sql(
                self._query.regras_formatadas_para_cache(self._client_id)
            ).fetchall()

        self._repo_db.dispose()

        column_names = [
            'id',
            'confianca',
            'suporte',
            'lift',
            'consequentes',
            'antecedentes',
        ]
        regras_df = DataFrame(result, columns=column_names)

        # O MSSQL não possui função de agregação para ARRAY, portanto, foi
        # criada uma concatenação de strings com colchetes para representar
        # uma estrutura de lista. A função json.dumps faz a conversão da
        # string concatenada para uma estrutura de listas em python.
        regras_df['antecedentes'] = regras_df['antecedentes'].apply(
            lambda x: json.loads(x)
        )
        regras_df['consequentes'] = regras_df['consequentes'].apply(
            lambda x: json.loads(x)
        )

        self._save_to_cache(regras_df.to_dict())

    @staticmethod
    def _format_decimal(value):
        return round(value, 2)

    @staticmethod
    def _format_list_to_string(lst):
        return ', '.join(map(str, lst))

    @staticmethod
    def _format_percentage(value):
        return round(100 * value, 2)

    @staticmethod
    def _create_rule_column(row):
        return f"{row['antecedents']} ==>> {row['consequents']}"

    def _save_to_cache(self, value: dict):
        self._repo_cache.insert_hash(
            key=CACHE_HASH,
            field=f'{self._client_id}-{MODEL_APRIORI}',
            value=json.dumps(value),
        )
