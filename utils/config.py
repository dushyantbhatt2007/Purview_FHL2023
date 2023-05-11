import json
import os

class ConfigError(Exception):
    """
    Exception raised when there is an error with the configuration.
    """
    pass


def load_config(path: str) -> dict:
    """
    Load configuration data from a JSON file.

    Args:
        path: A string containing the path to the JSON config file.

    Returns:
        A dictionary containing the configuration data.

    Raises:
        FileNotFoundError: If the config file is not found.
        JSONDecodeError: If the config file is not valid JSON.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(script_dir, path)
        with open(config_file, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print("Error: Config file not found.")
        raise
    except json.JSONDecodeError:
        print("Error: Config file is not valid JSON.")
        raise
