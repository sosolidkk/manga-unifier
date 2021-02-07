import os


def getenv_or_raise_exception(varname) -> str:
    """
    Retrieve a environment variable that MUST be set!
    """

    env = os.getenv(varname)
    if env is None:
        raise EnvironmentError(f"Environment variable {varname} is not set!")
    return env


def eval_env_as_boolean(varname, standard_value) -> bool:
    """
    Parse varname as bool and return it
    """
    return str(os.getenv(varname, standard_value)).lower() in ("true", "1", "t", "y")


def eval_env_as_integer(varname, standard_value) -> int:
    """
    Parse varname as int and return it
    """
    return int(os.getenv(varname, standard_value))


def eval_env_as_float(varname, standard_value) -> float:
    """
    Parse varname as float and return it
    """
    return float(os.getenv(varname, standard_value))
