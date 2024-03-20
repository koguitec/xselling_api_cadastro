import logging

from pydantic import ValidationError

from application.rest.adapters.request_adapter import HttpResponse

from .types import (
    BadRequestError,
    CacheEmptyError,
    ExpiredTokenError,
    NotFoundError,
    RegrasAssociacaoError,
    TokenInvalidError,
)

logger = logging.getLogger(__name__)


def handle_errors(error: Exception) -> HttpResponse:
    if isinstance(
        error,
        (
            BadRequestError,
            NotFoundError,
            ExpiredTokenError,
            TokenInvalidError,
            CacheEmptyError,
            RegrasAssociacaoError,
        ),
    ):
        logger.info(f'Handling known error: {error.name}')
        return HttpResponse(
            status_code=error.status_code,
            body={'errors': [{'title': error.name, 'message': error.message}]},
        )

    elif isinstance(error, (ValidationError,)):

        def format_pydantic_error(error):
            body = error.errors()[0]
            return f'{body["loc"][0]}: {body["msg"]}'

        logger.info('Handling ValidationError')
        return HttpResponse(
            status_code=422,
            body={
                'errors': [
                    {
                        'title': 'ValidationError',
                        'message': format_pydantic_error(error),
                    }
                ]
            },
        )

    logger.warning('Handling unknown error, returning ServerError')
    return HttpResponse(
        status_code=500,
        body={'errors': [{'title': 'ServerError', 'message': str(error)}]},
    )
