# <> with ❤️ by Micha Grandel - hello@michagrandel.eu

"""
BasicApplication provides a template class for a simple command line application

Use it to create a subclass and implement the main method.

Example:

    ```
    from typing import override
    from apppath import AppPath
    from plywoodpirate.application.BasicApplication import BasicApplication, Environment
    
    class MyApplication(BasicApplication):
        @override
        def _main(self, environment: Environment):
            print(environment.hello)
    
    def main():
        apppath = AppPath(app_name="my_app", app_author="plywoodpirate", app_version="1.0.0)
        app = MyApplication(apppath)
        app.run()
        
    if __name__ == "__main__":
        main()
    ```
"""

from __future__ import annotations

import logging
import platform
import sys
from argparse import ArgumentParser
from configparser import ConfigParser
from datetime import datetime
from os import PathLike
from pathlib import Path
from logging import DEBUG
from logging.handlers import RotatingFileHandler
from typing import Any, Optional

from apppath import AppPath

from ..logging import getLogger, StripAnsiFormatter, ColoredFormatter
from ..config import ConfigurationFile
from ..datetime import get_human_readable_time
from ..sys.platform import get_basic_system_info
from ..string import color as clicolor


logger = getLogger(__name__)

class Environment:
    """
    Namespace class for command line argument 
    
    The command line parser will add all parsed arguments to this class.
    """
    pass


class BasicApplication:
    """
    BasicApplication is a simple command line application.
    
    It provides some useful features, such as:
    
    * Logging to stdout and a log file
    * File rotation for log file
    * load configuration files
    * get system information
    * measure runtime and log it
    
    Arguments:
        environment (Environment): Namespace for command line arguments. (See also Environment-class)
        arg_parser (ArgumentParser): Command line argument parser.
        default_logging_config (Any): dataclass with default values for logging configuration.
    
    See also:
        Environment
    """
    def __init__(self, app: AppPath, log_level: int = DEBUG):
        self._app_path: AppPath = app
        self._log_level: int = log_level
        self._time_app_start: datetime = datetime.now()
        self._environment: Environment = Environment()
        self._arg_parser: ArgumentParser = ArgumentParser()
        self._default_logging_config: Any = None
        self._configuration_files: list[dict[str, Any]] = []

    @property
    def environment(self) -> Environment:
        return self._environment

    @property
    def arg_parser(self) -> ArgumentParser:
        return self._arg_parser

    @arg_parser.setter
    def arg_parser(self, value: ArgumentParser) -> None:
        self._arg_parser = value

    @arg_parser.deleter
    def arg_parser(self) -> None:
        del self._arg_parser

    @property
    def default_logging_config(self) -> Any:
        if self._default_logging_config is None:
            log_path = self._app_path.user_log
            class LoggingConfig:
                logfile: str = (log_path / "logging.log").as_posix()
                count: int = 3
                size: int = 5242880
            self._default_logging_config = LoggingConfig()
        return self._default_logging_config

    @default_logging_config.setter
    def default_logging_config(self, value: Any) -> None:
        self._default_logging_config = value

    @default_logging_config.deleter
    def default_logging_config(self) -> None:
        del self._default_logging_config

    def add_configuration_file(self, filename: str|PathLike, defaults: Any = None) -> None:
        """ 
        add a configuration file
        
        Args:
            filename (str|PathLike): configuration file name
            defaults (Any): ConfigParser or dataclass with default values
        """
        self._configuration_files.append({"file": filename, "default": defaults})

    def remove_configuration_file(self, filename: str|PathLike) -> None:
        """
        remove a configuration file
        
        Args:
            filename (str|PathLike): configuration file name
        """
        for configuration_file in self._configuration_files:
            if configuration_file["file"] == filename:
                self._configuration_files.remove(configuration_file)
                break

    def empty_configuration_files(self) -> None:
        """ empty configuration files """
        self._configuration_files = []

    def _debug_hardware_info(self, system_info):
        """ debug hardware info """
        self._print_debug_information({
            "cpu": system_info["cpu"],
            "memory": system_info["mem"],
            "disk": system_info["disk"],
        })

    def _debug_gpu_info(self, system_info):
        """ debug gpu info """
        self._print_debug_information({
            "gpu": system_info["gpu"],
        })

    def _debug_system_info(self, system_info):
        """ debug system info """
        self._print_debug_information({
            "python": system_info["python"],
            "script": system_info["script"],
            "version": system_info["version"],
            "hostname": system_info["hostname"],
            "platform": f"{system_info['platform']} ❤️" if system_info["platform"] == "Linux" else system_info["platform"],
        })

    def _debug_distro_info(self):
        """ debug distro info """
        distro = platform.freedesktop_os_release()
        distro_info = {
            "name": distro["NAME"],
            "version": distro["VERSION_ID"],
            "codename": distro["VERSION_CODENAME"],
            "support_end": distro["SUPPORT_END"],
        }
        distro_info_string = f"Running on {distro_info['name']} {distro_info['version']} {distro_info['codename']}"
        logger.debug(f"{distro_info_string}")
        support_end = datetime.strptime(distro_info["support_end"], "%Y-%m-%d")
        if support_end < datetime.now():
            distro_info_string += " (END OF SUPPORT)"
            logger.info(f"Thank you for using Linux! Please upgrade to a newer {distro_info['name']} release as soon as possible! Stay safe!")
        else:
            logger.info("❤️ Thank you for using Linux! ❤️")

    def _print_debug_information(self, info):
        """ print system debug information """
        info_string = ", ".join([f"{k}: {v}" for k, v in info.items()])
        logger.debug(f"{info_string}")

    def _debug_warnings(self, system_info):
        """ debug warnings """
        if system_info["mem_warning"]:
            left_free_message = clicolor.red(f"Free memory left: {system_info['memory']}")
            logger.warning(f"Please close some unneeded applications or upgrade your memory! {left_free_message}")
        if system_info["disk_warning"]:
            left_free_message = clicolor.red(f"Free disk space left: {system_info['disk']}")
            logger.warning(f"Please free up some disk space, it is getting quite full! {left_free_message}")


    def run(self) -> None:
        """
        run application

        This will trigger a series of operations. First, as a setup, the
        application initializes all required services, configures logging,
        loads the tool configuration, and parses the command line arguments.

        Finally, it will run the application code.

        After finishing, it will run some cleanup code and finishing tasks, 
        such as logging the runtime of the application.
        """
        self._time_app_start = datetime.now()
        environment:Environment = self._parse_commandline_arguments()

        for config in self._configuration_files:
            config_parser = self._load_configuration(config["file"], defaults=config["default"])
            config_name = Path(config["file"]).stem
            setattr(environment, config_name, config_parser)

        self._configure_logging(environment.logging)

        logger.info(f"Start {self._app_path.app_name} ...")
        basic_system_info = get_basic_system_info(self._app_path)

        self._debug_hardware_info(basic_system_info)
        self._debug_gpu_info(basic_system_info)

        if basic_system_info["platform"] == "Linux" and sys.version_info >= (3, 10):
            self._debug_distro_info()
        
        self._debug_warnings(basic_system_info)

        exit_code = self._main(environment)

        if exit_code is None:
            exit_code = 0
        self._quit(exit_code)

    def _configure_logging(self, configuration: ConfigParser):
        """
        Configure logging
        
        Args:
            configuration (ConfigParser): configuration parser for logging configuration
        """
        section_name = self._default_logging_config.__class__.__name__
        logfile = configuration.get("{section_name}", "logfile", fallback=self.default_logging_config.logfile)
        count = configuration.getint("{section_name}", "count", fallback=self.default_logging_config.count)
        size = configuration.getint("{section_name}", "size", fallback=self.default_logging_config.size)

        logger.setLevel(self._log_level)

        if logger.hasHandlers():
            logger.handlers.clear()

        stream_handler = logging.StreamHandler(stream=sys.stdout)
        format_ = '%(levelname)s: %(message)s'
        formatter = ColoredFormatter(fmt=format_)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        file_handler = RotatingFileHandler(logfile, maxBytes=size, backupCount=count)
        format_ = '%(asctime)s {"level"="%(levelname)s"} %(message)s'
        datefmt = "%Y-%m-%dT%H:%M:%S"
        formatter = StripAnsiFormatter(fmt=format_, datefmt=datefmt)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def _parse_commandline_arguments(self) -> Environment:
        """ parse command line arguments """
        environment = Environment()
        logger.debug("Parse arguments ...")
        self._arg_parser.parse_args(sys.argv[1:], environment)
        return environment

    def _load_configuration(self, filename: str|PathLike, defaults: Any = None) -> ConfigParser:
        """
        load configuration
        
        Args:
            filename (str|PathLike): configuration file name
            defaults (Any): ConfigParser or dataclass with default values
        """
        filepath = self._app_path.user_config / filename
        logger.debug(f"Load configuration {filepath.as_posix()} ...")
        config_file = ConfigurationFile(filepath)
        if defaults:
            config_file.set_default(defaults)
        return config_file.load()

    def _main(self, environment: Environment) -> Optional[int]:
        """
        main method for application code.
        This should be implemented by a subclass.
        
        Args:
            environment (Environment): namespace for command line arguments
        
        Returns:
            Optional[int]: exit code (0 = success, None = no exit code, anything else = failure)
        """
        pass

    def _quit(self, exit_code: int|str):
        """
        Quit application, log runtime and exit
        
        Args:
            exit_code (int|str): exit code
        """
        time_app_finished = datetime.now()
        duration = (time_app_finished - self._time_app_start).total_seconds()
        duration_as_text = get_human_readable_time(seconds=duration)
        logger.info(f"{self._app_path.app_name} has finished in {duration_as_text}")
        sys.exit(exit_code)
