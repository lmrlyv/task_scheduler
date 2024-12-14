from task_scheduler.helpers import get_env_var, str_to_bool


IS_DEV: bool = str_to_bool(get_env_var("IS_DEV"))
DJANGO_SECRET_KEY: str = get_env_var("DJANGO_SECRET_KEY", required=True)
