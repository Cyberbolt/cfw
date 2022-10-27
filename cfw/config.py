import yaml

from .CFWError import ConfigurationCFWError


with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def load_config():
    if not config.get("frequency"):
        raise ConfigurationCFWError(
            "The 'frequency' parameter does not exist."
        )
    if not config.get("max_num"):
        raise ConfigurationCFWError(
            "The 'max_num' parameter does not exist."
        )
    if not config.get("backup_time"):
        raise ConfigurationCFWError(
            "The 'backup_time' parameter does not exist."
        )
    if not config.get("unblock_time"):
        raise ConfigurationCFWError(
            "The 'unblock_time' parameter does not exist."
        )
    if not config.get("whitelist"):
        raise ConfigurationCFWError(
            "The 'whitelist' parameter does not exist."
        )
    if not config.get("blacklist"):
        raise ConfigurationCFWError(
            "The 'blacklist' parameter does not exist."
        )
    if not config.get("whitelist6"):
        raise ConfigurationCFWError(
            "The 'whitelist6' parameter does not exist."
        )
    if not config.get("blacklist6"):
        raise ConfigurationCFWError(
            "The 'blacklist6' parameter does not exist."
        )


load_config()
