"""Module for the Category serializer"""
import json


class CategoryJsonEncoder(json.JSONEncoder):
    """Serializer class for the category model

    Args:
        json (object): JSONEncoder

    Returns:
        str: serialized object
    """

    def default(self, o):
        try:
            to_serialize = {
                'id': o.id,
                'code': str(o.code),
                'descricao': o.descricao,
                'client_id': o.client_id,
                'dt_inclusao': str(o.dt_inclusao)
                if o.dt_inclusao is not None
                else o.dt_inclusao,
                'dt_alteracao': str(o.dt_alteracao)
                if o.dt_alteracao is not None
                else o.dt_alteracao,
                'ativo': o.ativo,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
