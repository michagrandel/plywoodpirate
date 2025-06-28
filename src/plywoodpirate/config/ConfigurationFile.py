# <> with ❤️ by Micha Grandel - hello@michagrandel.eu
""" Load configuration from file """

__all__ = ["ConfigurationFile"]

import copy
import os
from configparser import ConfigParser
from os import PathLike
from pathlib import Path
from typing import Optional, Any


class ConfigurationFile:
    """
    ConfigurationFile loads a configuration file and provides methods to access its values.
    
    It also provides methods to set up a default configuration. Use one ConfigFile object
    per configuration file.
    
    Attributes:
        filepath (PathLike): Path to a configuration file.
    
    Example:
    ```
    class Defaults:
        log_level: str = "INFO"
        log_file: str = "log.log"
        
    config_file_path = "config.conf"
    
    config_file = ConfigurationFile(config_file_path)
    config_file.set_default(Defaults)
    config_file.load()
    ```
    
    """
    def __init__(self, filepath: Optional[PathLike|str] = None,) -> None:
        """
        Args:
            filepath (PathLike|str): Path to a configuration file. 
        """
        filepath = filepath or os.curdir
        self._config_parser: ConfigParser = ConfigParser()
        self._filepath: Path = Path(filepath)

    @property
    def filepath(self) -> Path:
        return self._filepath

    @filepath.setter
    def filepath(self, filepath: PathLike|str) -> None:
        self._filepath = Path(filepath)

    @filepath.deleter
    def filepath(self) -> None:
        del self._filepath

    def set_default(self, data: Any) -> None:
        """
        Set the default configuration.
        
        If data is a ConfigParser, it will copy its values to the default configuration.
        Otherwise, data is expected to be a dataclass - an object with __dict__ attribute
        containing the default values.
        
        Args:
            data (Any): ConfigParser or object with default values.
        """

        if isinstance(data, ConfigParser):
            self.set_default_from_configparser(data)
        else:
            self.set_default_from_dataclass(data)

    def set_default_from_dataclass(self, dataclass: Any) -> None:
        """
        Set default configuration values using a dataclass.
        
        Dataclass can be of any object type, but it must have a __dict__ attribute.

        Args:
            dataclass (Any): object with default values.
        """
        class_name = dataclass.__name__
        config_parser = ConfigParser()
        config_parser.add_section(class_name)
        settings = (*filter(lambda a: not a.startswith("_"), dir(dataclass)),)
        for setting in settings:
            value = getattr(dataclass, setting)
            if isinstance(value, Path):
                value = value.as_posix()
            else:
                value = str(value)
            config_parser.set(class_name, setting, value)
        self._config_parser = config_parser

    def set_default_from_configparser(self, config_parser: ConfigParser) -> None:
        """
        Set default configuration values using a ConfigParser.

        Args:
            config_parser (ConfigParser): default configuration.
        """
        self._config_parser = copy.deepcopy(config_parser)
        print(id(self._config_parser))
        print(id(config_parser))

    def load(self, default: Any = None) -> ConfigParser:
        """
        Load configuration from a file.

        Args:
            filepath (PathLike): Path to a configuration file.
            default: optional dataclass with default values
            
        Returns:
            configparser.ConfigParser: loaded configuration.
        """
        if default:
            self.set_default(default)
        
        default_filepath = self._get_default_config_filename(self.filepath)
        Path(default_filepath.parent).mkdir(parents=True, exist_ok=True)

        with open(default_filepath, "w") as config_file:
            self._config_parser.write(config_file)

        self._config_parser.read([self.filepath, default_filepath], "utf-8")
        return self._config_parser

    def get(self, section: str, option: str, **kwargs) -> Any:
        return self._config_parser.get(section, option, **kwargs)

    def getint(self, section: str, option: str, **kwargs) -> int:
        return self._config_parser.getint(section, option, **kwargs)

    def getfloat(self, section: str, option: str, **kwargs) -> float:
        return self._config_parser.getfloat(section, option, **kwargs)

    def getboolean(self, section: str, option: str, **kwargs) -> bool:
        return self._config_parser.getboolean(section, option, **kwargs)

    def _get_default_config_filename(self, filepath: PathLike|str) -> Path:
        """
        The default configuration file is used to store the default values for a configuration file.

        Args:
            filepath (PathLike): Path to a configuration file.
        """

        filepath = Path(filepath)

        parent = filepath.parent
        stem = filepath.stem
        suffix = filepath.suffix

        return Path(Path(parent) / f"{stem}.default{suffix}")

