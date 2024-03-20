from ..strategies.concrete_strategy_apriory import AprioriRecommenderList
from ..strategies.concrete_strategy_implicit import ImplicitRecommenderList


class RecomendacaoListUseCase:
    """
    The `RecomendacaoListUseCase` class is responsible for executing a use case
    that retrieves recommended products based on a list of input products.

    Expected output:
        {
            "type": "Recomendacao",
            "count": <number_of_recommended_products>,
            "attributes": <recommended_products_list>
        }

    Methods:
    - execute(http_request: dict, client: dict) -> dict: Executes the use case
    by searching recommended products based on the input request and returns
    the formatted response.
    """

    ALGORITHMS = {
        'als': ImplicitRecommenderList,
        'apriori': AprioriRecommenderList,
    }

    def execute(self, http_request: dict, client: dict) -> dict:
        items_sku: list[str] = http_request['produtos_sku']
        algo_type: str = http_request['algoritmo']
        client_id: str = client['client_id']

        if algo_type not in self.ALGORITHMS:
            raise ValueError(f'Tipo de algoritmo não reconhecido: {algo_type}')

        # Decide qual algoritmo fazer a busca por recomendação
        recommender_class = self.ALGORITHMS[algo_type]
        recommender = recommender_class()
        result = recommender.execute(items_sku, client_id)

        return result
