from pydantic import BaseModel


class InternalServerError(BaseModel):
    type: str
    message: str

    class Config:
        json_schema_extra = {
            'example': {
                'error': [
                    {
                        'type': 'ServerError',
                        'message': 'Internal Server Error',
                    }
                ]
            }
        }


class UnprocessableEntityError(BaseModel):
    type: str
    message: str

    class Config:
        json_schema_extra = {
            'example': {
                'error': [
                    {
                        'type': 'ValidationError',
                        'message': 'Dado inválido',
                    }
                ]
            }
        }


class AutenticationError(BaseModel):
    class ErrorDetail(BaseModel):
        type: str
        message: str

    error: ErrorDetail

    class Config:
        json_schema_extra = {
            'example': {
                'error': {
                    'type': 'AuthenticationError',
                    'message': 'Token inválido',
                }
            }
        }


class DomainError(BaseModel):
    type: str
    message: str


class ClientDomainError(DomainError):
    class Config:
        json_schema_extra = {
            'example': {
                'error': [
                    {
                        'type': 'DomainAlreadyExistsError',
                        'message': 'O CNPJ já existe',
                    }
                ]
            }
        }


class CategoryDomainError(DomainError):
    class Config:
        json_schema_extra = {
            'example': {
                'error': [
                    {
                        'type': 'DomainAlreadyExistsError',
                        'message': 'Categoria já cadastrada',
                    }
                ]
            }
        }


class ProductDomainError(DomainError):
    class Config:
        json_schema_extra = {
            'example': {
                'error': [
                    {
                        'type': 'DomainAlreadyExistsError',
                        'message': 'Produto já cadastrada',
                    }
                ]
            }
        }
