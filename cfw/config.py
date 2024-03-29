import yaml

from .CFWError import ConfigurationCFWError


with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def load_config():
    if config.get("port") == None:
        raise ConfigurationCFWError(
            "The 'port' parameter does not exist."
        )
    if type(config.get("port")) != int:
        raise ConfigurationCFWError(
            "The 'port' parameter must be of integer type."
        )
        
    if config.get("frequency") == None:
        raise ConfigurationCFWError(
            "The 'frequency' parameter does not exist."
        )
    if type(config.get("frequency")) != int:
        raise ConfigurationCFWError(
            "The 'frequency' parameter must be of integer type."
        )
        
    if config.get("max_num") == None:
        raise ConfigurationCFWError(
            "The 'max_num' parameter does not exist."
        )
    if type(config.get("max_num")) != int:
        raise ConfigurationCFWError(
            "The 'max_num' parameter must be of integer type."
        )
        
    if config.get("backup_time") == None:
        raise ConfigurationCFWError(
            "The 'backup_time' parameter does not exist."
        )
    if type(config.get("backup_time")) != int:
        raise ConfigurationCFWError(
            "The 'backup_time' parameter must be of integer type."
        )
        
    if config.get("unblock_time") == None:
        raise ConfigurationCFWError(
            "The 'unblock_time' parameter does not exist."
        )
    if type(config.get("unblock_time")) != int:
        raise ConfigurationCFWError(
            "The 'unblock_time' parameter must be of integer type."
        )
    
    if config.get("whitelist") == None:
        raise ConfigurationCFWError(
            "The 'whitelist' parameter does not exist."
        )
    if config.get("whitelist").rsplit(".", 1)[1] != "txt":
        raise ConfigurationCFWError(
            "The whitelist file must be in 'txt' format."
        )
    if config.get("blacklist") == None:
        raise ConfigurationCFWError(
            "The 'blacklist' parameter does not exist."
        )
    if config.get("blacklist").rsplit(".", 1)[1] != "txt":
        raise ConfigurationCFWError(
            "The blacklist file must be in 'txt' format."
        )
    if config.get("whitelist6") == None:
        raise ConfigurationCFWError(
            "The 'whitelist6' parameter does not exist."
        )
    if config.get("whitelist6").rsplit(".", 1)[1] != "txt":
        raise ConfigurationCFWError(
            "The whitelist6 file must be in 'txt' format."
        )
    if config.get("blacklist6") == None:
        raise ConfigurationCFWError(
            "The 'blacklist6' parameter does not exist."
        )
    if config.get("blacklist6").rsplit(".", 1)[1] != "txt":
        raise ConfigurationCFWError(
            "The blacklist6 file must be in 'txt' format."
        )
    
    if config.get("log_file_path") == None:
        raise ConfigurationCFWError(
            "The 'log_file_path' parameter does not exist."
        )
    if config.get("log_file_path").rsplit(".", 1)[1] != "csv":
        raise ConfigurationCFWError(
            "The log file must be in 'csv' format."
        )
        
    if config.get("log_max_lines") == None:
        raise ConfigurationCFWError(
            "The 'log_max_lines' parameter does not exist."
        )
    if type(config.get("log_max_lines")) != int:
        raise ConfigurationCFWError(
            "The 'log_max_lines' parameter must be of integer type."
        )


load_config()
