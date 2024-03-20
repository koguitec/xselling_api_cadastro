# from flask import Blueprint

# blueprint = Blueprint('application', __name__)
# blueprint.add_url_rule('/clients', view_func=client_create, methods=['POST'])
# blueprint.add_url_rule('/clients', view_func=client_list, methods=['GET'])
# blueprint.add_url_rule('/clients', view_func=client_update, methods=['PUT'])
# blueprint.add_url_rule(
#     '/categories', view_func=category_create, methods=['POST']
# )
# blueprint.add_url_rule('/categories', view_func=category_list, methods=['GET'])
# blueprint.add_url_rule(
#     '/categories', view_func=category_update, methods=['PUT']
# )
# blueprint.add_url_rule('/products', view_func=product_create, methods=['POST'])
# blueprint.add_url_rule('/products', view_func=product_list, methods=['GET'])
# blueprint.add_url_rule('/products', view_func=product_update, methods=['PUT'])
# blueprint.add_url_rule(
#     '/transactions', view_func=transaction_create, methods=['POST']
# )
# blueprint.add_url_rule(
#     '/transactions', view_func=transaction_list, methods=['GET']
# )
from fastapi import APIRouter

from application.rest.schema.category import (
    CategoryRequest,
    UpdateCategoryRequest,
)
from application.rest.schema.client import ClientRequest, UpdateClientSchema
from application.rest.schema.product import ProductSchema, UpdateProductSchema
from application.rest.schema.transaction import TransactionRequest
from src.validators.recomendacao import (
    BadRequestError,
    NotFoundError,
    UnauthorizedError,
)

from .rest.category import category_create, category_list, category_update
from .rest.client import client_create, client_list, client_update
from .rest.product import product_create, product_list, product_update
from .rest.recomendacao import recomendacao_list
from .rest.schema.error import (
    CategoryDomainError,
    ClientDomainError,
    InternalServerError,
    ProductDomainError,
    UnprocessableEntityError,
)
from .rest.transaction import transaction_create, transaction_list

router = APIRouter()

# CLIENTES
router.add_api_route(
    '/clients',
    endpoint=client_create,
    methods=['POST'],
    tags=['Clientes'],
    responses={
        409: {'model': ClientDomainError},
        422: {'model': UnprocessableEntityError},
        500: {'model': InternalServerError},
    },
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ClientRequest.model_json_schema()
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/clients',
    endpoint=client_list,
    methods=['GET'],
    tags=['Clientes'],
    responses={500: {'model': InternalServerError}},
    openapi_extra={
        'parameters': [
            {
                'in': 'query',
                'name': 'id__eq',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'code__eq',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'ativo__eq',
                'required': False,
                'schema': {'type': 'boolean'},
            },
            {
                'in': 'query',
                'name': 'cnpj__eq',
                'required': False,
                'schema': {'type': 'string'},
            },
        ]
    },
)
router.add_api_route(
    '/clients',
    endpoint=client_update,
    methods=['PUT'],
    tags=['Clientes'],
    responses={
        422: {'model': UnprocessableEntityError},
        500: {'model': InternalServerError},
    },
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': UpdateClientSchema.model_json_schema()
                }
            },
            'required': True,
        },
    },
)

# CATEGORIAS
router.add_api_route(
    '/categories',
    endpoint=category_create,
    methods=['POST'],
    tags=['Categorias'],
    responses={
        409: {'model': CategoryDomainError},
        422: {'model': UnprocessableEntityError},
        500: {'model': InternalServerError},
    },
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': CategoryRequest.model_json_schema()
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/categories',
    endpoint=category_list,
    methods=['GET'],
    tags=['Categorias'],
    responses={500: {'model': InternalServerError}},
    openapi_extra={
        'parameters': [
            {
                'in': 'query',
                'name': 'id__eq',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'code__eq',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'ativo__eq',
                'required': False,
                'schema': {'type': 'boolean'},
            },
            {
                'in': 'query',
                'name': 'client_id__eq',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'descricao__eq',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'page__eq',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'items_per_page__eq',
                'required': False,
                'schema': {'type': 'string'},
            },
        ]
    },
)
router.add_api_route(
    '/categories',
    endpoint=category_update,
    methods=['PUT'],
    tags=['Categorias'],
    responses={
        422: {'model': UnprocessableEntityError},
        500: {'model': InternalServerError},
    },
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': UpdateCategoryRequest.model_json_schema()
                }
            },
            'required': True,
        },
    },
)

# PRODUTOS
router.add_api_route(
    '/products',
    endpoint=product_create,
    methods=['POST'],
    tags=['Produtos'],
    responses={
        422: {'model': UnprocessableEntityError},
        409: {'model': ProductDomainError},
        500: {'model': InternalServerError},
    },
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': ProductSchema.model_json_schema()
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/products',
    endpoint=product_list,
    methods=['GET'],
    tags=['Produtos'],
    responses={500: {'model': InternalServerError}},
    openapi_extra={
        'parameters': [
            {
                'in': 'query',
                'name': 'id__eq',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'code__eq',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'ativo__eq',
                'required': False,
                'schema': {'type': 'boolean'},
            },
            {
                'in': 'query',
                'name': 'page__eq',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'items_per_page__eq',
                'required': False,
                'schema': {'type': 'string'},
            },
        ]
    },
)
router.add_api_route(
    '/products',
    endpoint=product_update,
    methods=['PUT'],
    tags=['Produtos'],
    responses={
        422: {'model': UnprocessableEntityError},
        500: {'model': InternalServerError},
    },
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': UpdateProductSchema.model_json_schema()
                }
            },
            'required': True,
        },
    },
)

# TRANSAÇÕES
router.add_api_route(
    '/transactions',
    endpoint=transaction_create,
    methods=['POST'],
    tags=['Transações'],
    responses={
        401: {'model': InternalServerError},
        422: {'model': UnprocessableEntityError},
        500: {'model': InternalServerError},
    },
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': TransactionRequest.model_json_schema()
                }
            },
            'required': True,
        },
    },
)
router.add_api_route(
    '/transactions',
    endpoint=transaction_list,
    methods=['GET'],
    tags=['Transações'],
    responses={
        401: {'model': InternalServerError},
        500: {'model': InternalServerError},
    },
    openapi_extra={
        'parameters': [
            {
                'in': 'query',
                'name': 'id__eq',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'code__eq',
                'required': False,
                'schema': {'type': 'integer'},
            },
            {
                'in': 'query',
                'name': 'ativo__eq',
                'required': False,
                'schema': {'type': 'boolean'},
            },
            {
                'in': 'query',
                'name': 'produto_id__eq',
                'required': False,
                'schema': {'type': 'boolean'},
            },
            {
                'in': 'query',
                'name': 'client_id__eq',
                'required': False,
                'schema': {'type': 'boolean'},
            },
            {
                'in': 'query',
                'name': 'page__eq',
                'required': False,
                'schema': {'type': 'string'},
            },
            {
                'in': 'query',
                'name': 'items_per_page__eq',
                'required': False,
                'schema': {'type': 'string'},
            },
        ]
    },
)

# RECOMENDAÇÃO
router.add_api_route(
    '/regras-ia-recomendacao',
    endpoint=recomendacao_list,
    methods=['POST'],
    responses={
        400: {'model': BadRequestError},
        401: {'model': UnauthorizedError},
        404: {'model': NotFoundError},
        422: {'model': UnprocessableEntityError},
        500: {'model': InternalServerError},
    },
    name='Recomendação de produtos baseado em regras de IA.',
    openapi_extra={
        'requestBody': {
            'content': {
                'application/json': {
                    'schema': {
                        'required': ['algoritmo', 'produtos_sku'],
                        'type': 'object',
                        'properties': {
                            'algoritmo': {'type': 'string'},
                            'produtos_sku': {
                                'type': 'array',
                                'items': {'type': 'string'},
                            },
                        },
                    }
                }
            },
            'required': True,
        },
    },
    tags=['Recomendação de produtos'],
)


def init_app(app):
    app.include_router(router)
    # app.register_blueprint(blueprint)
