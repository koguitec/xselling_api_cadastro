from fastapi import Request
from fastapi.responses import JSONResponse

from src.errors.error_handler import handle_errors
from src.validators.recomendacao import (
    RecomendacaoResponse,
    recomendacao_validate_schema,
)

from .adapters.request_adapter import request_adapter_recommendation
from .composers.recomendacao_list_composer import recomendacao_list_composer


async def recomendacao_list(request: Request) -> RecomendacaoResponse:
    try:
        await recomendacao_validate_schema(request)
        http_response = await request_adapter_recommendation(
            request, recomendacao_list_composer()
        )
    except Exception as exc:
        http_response = handle_errors(exc)
    return JSONResponse(http_response.body, http_response.status_code)
