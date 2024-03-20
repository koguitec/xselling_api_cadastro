from application.rest.adapters.request_adapter import (
    HttpRequest,
    HttpResponse,
    HttpStatusCode,
)
from src.plugins.jwt_plugin import auth_token
from src.use_cases.recomendacao_list import RecomendacaoListUseCase

from .interfaces.controller_interface import ControllerInterface


class RecomendacaoListController(ControllerInterface):
    def __init__(self, use_case: RecomendacaoListUseCase):
        self._use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        client: dict = auth_token.validate_token(http_request=http_request)

        result: list[dict] = self._use_case.execute(
            http_request=http_request.json, client=client
        )

        return HttpResponse(status_code=HttpStatusCode.OK.value, body=result)
