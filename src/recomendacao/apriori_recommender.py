from pandas import DataFrame

from src.drivers.apriori_recommender import apriori_driver
from src.errors.types import RegrasAssociacaoError


class AprioriRecommender:
    """
    A class for generating association rules using the Apriori algorithm.

    Attributes:
        _produtos_list (list): The list of products to be used in the Apriori
        algorithm.
        _min_support (float): The minimum support value for generating
        association rules.
        _min_threshold (float): The minimum threshold value for generating
        association rules.
        _metric (str): The metric to be used for evaluating the association
        rules.
        apriori_driver (Apriori): An instance of the Apriori class used for
        executing the Apriori algorithm.
    """

    def __init__(
        self,
        min_support: float,
        min_threshold: float,
        metric: str,
    ) -> None:
        """
        Initializes the AprioriRecommender instance with the specified minimum
        support, minimum threshold, and metric.

        Args:
            min_support (float): The minimum support value for generating
            association rules.
            min_threshold (float): The minimum threshold value for generating
            association rules.
            metric (str): The metric to be used for evaluating the association
            rules.
        """
        self._training_data = None
        self._min_support = min_support
        self._min_threshold = min_threshold
        self._metric = metric
        self._apriori_driver = apriori_driver

    def execute(self):
        """
        Executes the Apriori algorithm and returns the generated association
        rules as a DataFrame.

        Returns:
            DataFrame: The generated association rules.
        """
        matrix_incidencia: DataFrame = self._cria_matriz_incidencia(
            produtos=self._training_data
        )
        conjunto_produtos: DataFrame = self._cria_conjuntos_de_produtos(
            matrix_incidencia=matrix_incidencia
        )
        regras_associacao: DataFrame = self._cria_regras_associacao(
            conjunto_produtos=conjunto_produtos
        )

        return regras_associacao

    def set_parameters(self, training_data: list[list]):
        """
        Sets the list of products to be used in the Apriori algorithm.

        Args:
            produtos_list (list[list]): The list of products.
        """
        self._training_data = training_data

    def _cria_matriz_incidencia(self, produtos: list) -> DataFrame:
        """
        Creates the incidence matrix based on the list of products.

        Args:
            produtos (list): The list of products.

        Returns:
            DataFrame: The incidence matrix.
        """
        return self._apriori_driver.matriz_incidencia(produtos=produtos)

    def _cria_conjuntos_de_produtos(
        self,
        matrix_incidencia: DataFrame,
        use_colnames=True,
    ) -> DataFrame:
        """
        Creates the sets of products based on the incidence matrix and the
        specified minimum support.

        Args:
            matrix_incidencia (DataFrame): The incidence matrix.
            use_colnames (bool, optional): Whether to use column names for the
            sets of products. Defaults to True.

        Returns:
            DataFrame: The sets of products.
        """
        conjunto_produtos = self._apriori_driver.apriori(
            matrix_incidencia=matrix_incidencia,
            min_support=self._min_support,
            use_colnames=use_colnames,
        )
        if conjunto_produtos.empty:
            raise RegrasAssociacaoError(
                'Não foram encontrados conjuntos de produtos'
            )
        return conjunto_produtos

    def _cria_regras_associacao(
        self,
        conjunto_produtos: DataFrame,
    ) -> DataFrame:
        """
        Creates the association rules based on the sets of products and the
        specified minimum threshold and metric.

        Args:
            conjunto_produtos (DataFrame): The sets of products.

        Returns:
            DataFrame: The association rules.
        """
        regras_associacao = self._apriori_driver.association_rules(
            conjuntos_produtos=conjunto_produtos,
            metric=self._metric,
            min_threshold=self._min_threshold,
        )
        if regras_associacao.empty:
            raise RegrasAssociacaoError(
                'Não foram encontradas regras de associação'
            )
        return regras_associacao
