from task_scheduler.helpers import get_env_var


IS_DEBUG_ON: bool = get_env_var("ENVIRONMENT", required=True).lower() == "dev"
DJANGO_SECRET_KEY: str = get_env_var("DJANGO_SECRET_KEY", required=True)
