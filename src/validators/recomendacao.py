from fastapi import Request
from pydantic import BaseModel


class RecomendacaoRequest(BaseModel):
    algoritmo: str
    produtos_sku: list[str]


class RecomendacaoResponse(BaseModel):
    type: str
    count: int
    attributes: list[dict]


class HttpError(BaseModel):
    class Error(BaseModel):
        title: str
        message: str

    errors: list[Error]


class BadRequestError(HttpError):
    class Config:
        json_schema_extra = {
            'example': {
                'errors': [
                    {'title': 'BadRequest', 'message': 'Bad Request Error'}
                ]
            }
        }


class UnauthorizedError(HttpError):
    class Config:
        json_schema_extra = {
            'example': {
                'errors': [
                    {'title': 'Unauthorized', 'message': 'Unauthorized Error'}
                ]
            }
        }


class NotFoundError(HttpError):
    class Config:
        json_schema_extra = {
            'example': {
                'errors': [{'title': 'NotFound', 'message': 'Not Found Error'}]
            }
        }


class UnprocessableEntityError(HttpError):
    class Config:
        json_schema_extra = {
            'example': {
                'errors': [
                    {
                        'title': 'ValidationError',
                        'message': 'Unprocessable Entity Error',
                    }
                ]
            }
        }


class InternalServerError(HttpError):
    class Config:
        json_schema_extra = {
            'example': {
                'errors': [
                    {
                        'title': 'ServerError',
                        'message': 'Internal Server Error',
                    }
                ]
            }
        }


async def recomendacao_validate_schema(request: Request):
    request_body = await request.body()
    RecomendacaoRequest.parse_raw(request_body)
