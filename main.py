# Initialize ModelManager during application startup for pre-loading models
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.model_manager import ModelManager
from src.repository.postgres.base_postgresrepo import BasePostgresRepo

global_model_manager = ModelManager(
    repo_db=BasePostgresRepo(), repo_cache=RedisRepository()
)
global_model_manager.load_models_from_cache()
