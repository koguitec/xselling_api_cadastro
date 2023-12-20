"""Module for the Transaction serializer"""
import json


class TransactionJsonEncoder(json.JSONEncoder):
    """Serializer class for the transaction model

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
                'client_id': o.client_id,
                'dt_transacao': str(o.dt_transacao)
                if o.dt_transacao is not None
                else o.dt_transacao,
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
