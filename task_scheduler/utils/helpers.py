from os import getenv

from task_scheduler.utils.exceptions import ConfigError


def get_env_var(env_var_name: str, default: str = "", required: bool = False) -> str:
    """Get the value of an environment variable.

    Args:
        env_var_name (str): The name of the environment variable.
        default (str, optional): The default value to return if the environment variable is
            missing. Defaults to "".
        required (bool, optional): Whether the environment variable is required. Defaults to False.

    Raises:
        ConfigError: If the environment variable is required but not found.

    Returns:
        str: The value of the environment variable or the default value if not required.
    """
    value = getenv(env_var_name)

    if required and value is None:
        raise ConfigError(f"Environment variable '{env_var_name}' is required but not set.")

    return value.strip() if value is not None else default


def str_to_bool(value: str) -> bool:
    """Convert a string to a boolean.

    Args:
        value (str): The string to convert.

    Raises:
        ValueError: If the value cannot be converted to a boolean.

    Returns:
        bool: The boolean representation of the string.
    """
    if not isinstance(value, str):
        raise ValueError(f"Expected a string, got {type(value).__name__}.")

    value = value.strip().lower()

    if value in {"true", "yes", "1"}:
        return True
    elif value in {"false", "no", "0"}:
        return False
    else:
        raise ValueError(f"Cannot convert '{value}' to a boolean.")
