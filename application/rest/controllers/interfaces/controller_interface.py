from abc import ABC, abstractmethod

from application.rest.adapters.request_adapter import HttpRequest, HttpResponse


class ControllerInterface(ABC):
    @abstractmethod
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        ...
