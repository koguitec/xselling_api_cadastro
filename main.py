# Initialize ModelManager during application startup for pre-loading models
import logging

from src.errors.types.cache_empty import CacheEmptyError
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.model_manager import ModelManager
from src.repository.postgres.base_postgresrepo import BasePostgresRepo

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

try:
    global_model_manager = ModelManager(
        repo_db=BasePostgresRepo(), repo_cache=RedisRepository()
    )
    global_model_manager.load_models_from_cache()
except CacheEmptyError as e:
    logger.error(e)
