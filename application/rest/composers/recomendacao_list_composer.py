from src.use_cases.recomendacao_list import RecomendacaoListUseCase

from ..controllers.recomendacao_list_controller import (
    RecomendacaoListController,
)


def recomendacao_list_composer():

    recomendacao_use_case = RecomendacaoListUseCase()

    controller = RecomendacaoListController(recomendacao_use_case)

    return controller.handle
