from os import getenv

IS_DEV = getenv("IS_DEV", "").lower() in ["true", "1"]
