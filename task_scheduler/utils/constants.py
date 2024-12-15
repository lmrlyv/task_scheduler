from task_scheduler.utils.helpers import get_env_var


IS_DEBUG_ON: bool = get_env_var("ENVIRONMENT", required=True).lower() == "dev"
DJANGO_SECRET_KEY: str = get_env_var("DJANGO_SECRET_KEY", required=True)

CELERY_BROKER_HOST: str = get_env_var("CELERY_BROKER_HOST", required=True)
CELERY_BROKER_PORT: str = get_env_var("CELERY_BROKER_PORT", required=True)
CELERY_BROKER_USER: str = get_env_var("CELERY_BROKER_USER", required=True)
CELERY_BROKER_PASSWORD: str = get_env_var("CELERY_BROKER_PASSWORD", required=True)

DB_HOST: str = get_env_var("DB_HOST", required=True)
DB_PORT: str = get_env_var("DB_PORT", required=True)
DB_NAME: str = get_env_var("DB_NAME", required=True)
DB_USER: str = get_env_var("DB_USER", required=True)
DB_PASSWORD: str = get_env_var("DB_PASSWORD", required=True)
