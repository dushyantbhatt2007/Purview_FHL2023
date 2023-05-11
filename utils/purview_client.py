from pyapacheatlas.core import PurviewClient
import functools

from utils.config import load_config, ConfigError
from utils.auth import get_credential, AuthenticationError


class PurviewClientError(Exception):
    """
    Exception raised when there is an error with the Purview client.
    """
    pass


def get_purview_client(config_path: str) -> PurviewClient:
    """
    Create a Purview client object with the specified configuration and credentials.

    Args:
        config_path: A string containing the path to the JSON config file.

    Returns:
        A PurviewClient object representing the Purview client.

    Raises:
        PurviewClientError: If there is an error with the Purview client.
    """
    try:
        config = load_config(config_path)
        account_name = config.get("purview_account")
        if not account_name:
            raise ConfigError("Error: Purview account name missing from config.")

        credential = get_credential()

        client = PurviewClient(
            account_name=account_name,
            authentication=credential
        )

        return client

    except ConfigError as e:
        print(str(e))
        raise PurviewClientError(str(e))
    except AuthenticationError as e:
        print(str(e))
        raise PurviewClientError(str(e))


def with_purview_client(func):
    """
    A decorator to provide a PurviewClient object to a function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        client = get_purview_client("../config/config.json")
        return func(client, *args, **kwargs)

    return wrapper
