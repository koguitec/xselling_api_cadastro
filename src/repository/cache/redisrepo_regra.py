import os

from redis import Redis


class RedisRepository:
    """Repository class for redis"""

    def __init__(self):
        self._redis_conn = Redis(
            host=os.environ['REDIS_HOST'],
            port=os.environ['REDIS_PORT'],
            password=os.environ['REDIS_PASSWORD'],
        )

    def insert(self, key: str, value: any) -> None:
        self._redis_conn.set(key, value)

    def get(self, key: str) -> any:
        value = self._redis_conn.get(key)
        if value:
            return value.decode('utf-8')

    def insert_hash(self, key: str, field: str, value: any) -> None:
        self._redis_conn.hset(key, field, value)

    def get_hash(self, key: str, field: str) -> any:
        value = self._redis_conn.hget(key, field)
        try:
            return value.decode('utf-8')
        except Exception:
            return value
        # TODO melhorar esse condicional de retorno
