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
        """Insert a key-value pair into Redis

        Args:
            key (str): The key under which the data will be stored in Redis.
            value (any): The value to store in Redis.

        Returns:
            None
        """
        self._redis_conn.set(key, value)

    def get(self, key: str) -> any:
        """Retrieve a value by key from Redis

        Args:
            key (str): The key whose value is to be retrieved.

        Returns:
            any: The value corresponding to the given key if found, else None.
        """
        value = self._redis_conn.get(key)
        if value:
            return value.decode('utf-8')

    def insert_hash(self, key: str, field: str, value: any) -> None:
        """Insert a field-value pair to a hash stored in Redis under the provided key

        Args:
            key (str): The key under which the hash is stored.
            field (str):  The field within the hash to set a value for.
            value (any): The value to set for the given field in the hash.

        Returns:
            None
        """
        self._redis_conn.hset(key, field, value)

    def get_hash(self, key: str, field: str) -> any:
        """Retrieve a value by field from a hash stored in Redis under the provided key

        Args:
            key (str): The key under which the hash is stored.
            field (str): The field within the hash whose value is to be retrieved.

        Returns:
            any: The value corresponding to the given field in the hash if found, else None.
        """
        value = self._redis_conn.hget(key, field)
        try:
            return value.decode('utf-8')
        except Exception:
            return value
        # TODO melhorar esse condicional de retorno

    def pipeline(self):
        """Create a pipeline to execute multiple Redis commands in sequence without
        waiting for the replies and then retrieve all the replies at once.

        Returns:
            pipeline: Returns a pipeline object
        """
        return self._redis_conn.pipeline()
