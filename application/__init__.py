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

from .rest.category import category_create, category_list, category_update
from .rest.client import client_create, client_list, client_update
from .rest.product import product_create, product_list, product_update
from .rest.transaction import transaction_create, transaction_list

router = APIRouter()

router.add_api_route(
    '/clients', endpoint=client_create, methods=['POST'], tags=['Clientes']
)
router.add_api_route(
    '/clients', endpoint=client_list, methods=['GET'], tags=['Clientes']
)
router.add_api_route(
    '/clients', endpoint=client_update, methods=['PUT'], tags=['Clientes']
)
router.add_api_route(
    '/categories',
    endpoint=category_create,
    methods=['POST'],
    tags=['Categorias'],
)
router.add_api_route(
    '/categories',
    endpoint=category_list,
    methods=['GET'],
    tags=['Categorias'],
)
router.add_api_route(
    '/categories',
    endpoint=category_update,
    methods=['PUT'],
    tags=['Categorias'],
)
router.add_api_route(
    '/products', endpoint=product_create, methods=['POST'], tags=['Produtos']
)
router.add_api_route(
    '/products', endpoint=product_list, methods=['GET'], tags=['Produtos']
)
router.add_api_route(
    '/products', endpoint=product_update, methods=['PUT'], tags=['Produtos']
)
router.add_api_route(
    '/transactions',
    endpoint=transaction_create,
    methods=['POST'],
    tags=['Transações'],
)
router.add_api_route(
    '/transactions',
    endpoint=transaction_list,
    methods=['GET'],
    tags=['Transações'],
)


def init_app(app):
    app.include_router(router)
    # app.register_blueprint(blueprint)
