from pandas import DataFrame
from scipy.sparse import csr_matrix

from src.drivers.implicit_recommender import MatrixBuilder, implicit_driver


class ImplicitRecommender:
    """
    Recommender system class that builds and trains a recommender system using
    implicit feedback data.

    Args:
        algo_type (str): The algorithm type for the recommender.
        matrix_builder (MatrixBuilder): An instance of the MatrixBuilder class.

    Attributes:
        _client_products_df (DataFrame): The input data as a DataFrame.
        _algo_type (str): The algorithm type for the recommender.
        _matrix_builder (MatrixBuilder): An instance of the MatrixBuilder class.
        _implicit_driver (implicit_driver): The implicit recommender model.

    """

    def __init__(self, params: dict, matrix_builder: MatrixBuilder) -> None:
        """
        Initializes the ImplicitRecommender instance with the algorithm type
        and matrix builder.

        Args:
            algo_type (str): The algorithm type for the recommender.
            matrix_builder (MatrixBuilder): An instance of the MatrixBuilder
            class.

        Returns:
            None
        """
        self._training_data = None
        self._matrix_builder = matrix_builder
        self._implicit_driver = implicit_driver.build_recommender(
            algo_type=params['algo_type']
        )

    def execute(self):
        """
        Executes the recommendation process by building the client products
        matrix, applying matrix weighting,
        fitting the model, and generating recommendations.

        Returns:
            implicit_model: The choosen trained model
        """
        interaction_matrix, item_to_index = self._build_csr_matrix(
            client_products_df=self._training_data
        )
        client_products_matrix = self._matrix_weighting(
            interaction_matrix=interaction_matrix
        )
        self._fit(client_products_matrix=client_products_matrix)

        return self._implicit_driver.implicit_model, item_to_index

    def set_parameters(self, training_data: DataFrame):
        """
        Sets the input data as a DataFrame.

        Args:
            training_data (DataFrame): The input data as a DataFrame.

        Returns:
            None
        """
        if not isinstance(training_data, DataFrame):
            raise TypeError(
                f'Expecting type of DataFrame, received {type(training_data)}'
            )
        self._training_data = training_data

    def _build_csr_matrix(self, client_products_df: DataFrame):
        """
        Builds a CSR matrix from the client products DataFrame using the matrix
        builder.

        Args:
            client_products_df (DataFrame): The client products DataFrame.

        Returns:
            csr_matrix: The CSR matrix representation of the client products
            DataFrame.
        """
        return self._matrix_builder.build_csr_matrix(
            client_products_df=client_products_df
        )

    def _matrix_weighting(
        self, interaction_matrix: csr_matrix, method='bm25', K1=10, B=0.8
    ):
        """
        Applies matrix weighting to the interaction matrix using the specified
        method, K1, and B parameters.

        Args:
            interaction_matrix (csr_matrix): The interaction matrix.
            method (str, optional): The matrix weighting method. Defaults to 'bm25'.
            K1 (int, optional): The K1 parameter. Defaults to 10.
            B (float, optional): The B parameter. Defaults to 0.8.

        Returns:
            csr_matrix: The weighted interaction matrix.
        """
        return self._implicit_driver.matrix_weighting(
            interaction_matrix=interaction_matrix, method=method, K1=K1, B=B
        )

    def _fit(self, client_products_matrix: csr_matrix) -> None:
        """
        Fits the model to the client products matrix.

        Args:
            client_products_matrix (csr_matrix): The client products matrix.

        Returns:
            None
        """
        self._implicit_driver.fit(
            client_products_matrix=client_products_matrix
        )
