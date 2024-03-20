import json
from itertools import chain

from src.errors.types import CacheEmptyError, NotFoundError
from src.interfaces.recommender import AlgorithmStrategyInterface
from src.recomendacao.training_pipeline import CACHE_HASH, MODEL_APRIORI
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.postgres.postgresrepo_product import PostgresRepoProduct


class AprioriRecommenderList(AlgorithmStrategyInterface):
    def __init__(self) -> None:
        self._recomendacao_repository = PostgresRepoProduct()
        self._repo_cache = RedisRepository()

    def execute(self, items_sku, client_id):
        categoria_ids = self._search_categorias_on_cache(items_sku=items_sku)

        regras = self._search_regras_on_cache(
            categoria_ids=categoria_ids, client_id=client_id
        )
        consequente_ids = self._search_consequentes_on_cache(
            regras=regras, client_id=client_id
        )
        recomendacao = self._search_produtos_recomendados_on_cache(
            consequente_ids=consequente_ids, items_sku=items_sku
        )
        return self._format_response(recomendacao=recomendacao, regras=regras)

    def _search_categorias_on_cache(self, items_sku: list[str]) -> list[int]:
        """Busca das categorias dos produtos

        Args:
            items_sku (list[str]): Lista com sku dos produtos

        Raises:
            NotFoundError: "Não existem categorias para os produtos relacionados"

        Returns:
            list[int]: Lista com ids das categorias
        """
        sku_to_prod = self._repo_cache.get_hash(CACHE_HASH, 'sku_to_item')

        if sku_to_prod is None:
            raise CacheEmptyError('Mapper sku_to_item não encontrado no cache')

        sku_to_prod = json.loads(sku_to_prod)

        # Using a list comprehension to retrieve 'id' values for the specified keys
        category_ids: list[int] = [
            sku_to_prod[key]['id'] for key in sku_to_prod if key in items_sku
        ]

        if category_ids == []:
            raise NotFoundError(
                'Não existem categorias para os produtos relacionados'
            )
        return category_ids

    def _search_regras_on_cache(
        self, categoria_ids: list[int], client_id: str
    ) -> list[int]:
        """Busca das regras através das categorias dos produtos

        Args:
            categoria_ids (list[int]): List com ids das categorias

        Raises:
            NotFoundError: "Não há regras para o produto"

        Returns:
            list[int]: Lista com as regras cadastradas
        """
        result: dict = self._get_data_from_cache(client_id)

        matching_regras_ids = []

        categoria_ids_set = set(categoria_ids)

        for antecedente_key, antecedente_value in result[
            'antecedentes'
        ].items():
            if set(antecedente_value).issubset(categoria_ids_set):
                matching_regras_ids.append(
                    {
                        key: antecedente_value[antecedente_key]
                        for key, antecedente_value in result.items()
                    }
                )

        if matching_regras_ids == []:
            raise NotFoundError('Não há regras para o produto')
        return matching_regras_ids

    def _search_consequentes_on_cache(
        self, regras: list[dict], client_id: str
    ) -> list[int]:
        """Busca das categorias consequentes através do ID das regras

        Args:
            regra_ids (list[int]): Lista com ids das regras

        Raises:
            NotFoundError: "Não há categorias recomendados pela IA"

        Returns:
            list[int]: Lista de categorias de consequentes
        """
        result: dict = self._get_data_from_cache(client_id)

        matching_consequentes = []

        regra_ids = [r['id'] for r in regras]

        for key, value in result['id'].items():
            if value in regra_ids:
                matching_consequentes.append(result['consequentes'][key])
        if matching_consequentes == []:
            raise NotFoundError('Não há categorias recomendados pela IA')

        return list(set(chain(*matching_consequentes)))

    def _search_produtos_recomendados_on_cache(
        self, consequente_ids: list[int], items_sku: list[str]
    ) -> list[dict]:
        """Busca de produtos recomendados

        Args:
            consequente_ids (list[int]): Lista com ids das categorias recomendadas

        Raises:
            NotFoundError: "Não há produtos recomendados pela IA"

        Returns:
            list[dict]: Lista de dicionários com produtos recomendados
        """
        cat_id_to_prods = self._repo_cache.get_hash(
            CACHE_HASH, 'cat_id_to_items'
        )

        if cat_id_to_prods is None:
            raise CacheEmptyError(
                'Mapper cat_id_to_items não encontrado no cache'
            )

        cat_id_to_prods = json.loads(cat_id_to_prods)

        recomendacao = [
            item
            for cat_id in consequente_ids
            if str(cat_id) in cat_id_to_prods
            for item in cat_id_to_prods[str(cat_id)]
            if item['sku'] not in items_sku
        ]

        if recomendacao == []:
            raise NotFoundError('Não há produtos recomendados pela IA')
        return recomendacao

    @staticmethod
    def _format_response(*, recomendacao: list[dict], regras: list[dict]):
        """Formatação do payload de resposta

        Args:
            recomendacao (list[dict]): Lista de dicionários com produtos recomendados

        Returns:
            dict: Dicionário formatado com produtos recomendados
        """
        for product in recomendacao:
            for regra in regras:
                if (
                    product['categoria_id'] in regra['consequentes']
                    and 'lift' not in product
                ) or ('lift' in product and product['lift'] < regra['lift']):
                    product.update(
                        {
                            'confianca': regra['confianca'],
                            'lift': regra['lift'],
                            'suporte': regra['suporte'],
                            'regra_id': regra['id'],
                        }
                    )

        for item in recomendacao:
            del item['categoria_id']

        result = {
            'type': 'Recomendacao - Apriori',
            'count': len(recomendacao),
            'attributes': recomendacao,
        }
        return result

    def _get_data_from_cache(self, client_id: str) -> dict:
        result = self._repo_cache.get_hash(
            CACHE_HASH, f'{client_id}-{MODEL_APRIORI}'
        )
        if result is None:
            raise CacheEmptyError('Não foram encontradas regras no cache')
        return json.loads(result)
