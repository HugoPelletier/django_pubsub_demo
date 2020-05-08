import json
import logging
import sys
from typing import List, Dict, Union


class LoggerUtils:

    std_out = None
    std_err = None

    # Here will be the instance stored.
    instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if LoggerUtils.instance is None:
            LoggerUtils()
        return LoggerUtils.instance

    def __init__(self):
        """ Virtually private constructor. """
        if LoggerUtils.instance is None:
            # set stdout
            self.std_out = logging.getLogger('serverless-pubsub')
            self.std_out.setLevel(logging.DEBUG)
            self.std_out.addHandler(logging.StreamHandler(sys.stdout))
            self.std_out.propagate = False

            # set stderr
            self.std_err = logging.getLogger('serverless-pubsub')
            self.std_err.setLevel(logging.DEBUG)
            self.std_err.addHandler(logging.StreamHandler(sys.stderr))
            self.std_err.propagate = False

            LoggerUtils.instance = self

    @classmethod
    def debug(cls, msg: Union[str, Dict], *args: List, **kwargs: Dict) -> None:
        LoggerUtils.instance.std_out.debug(cls.format_input(msg), *args, **kwargs)

    @classmethod
    def info(cls, msg: Union[str, Dict], *args: List, **kwargs: Dict) -> None:
        LoggerUtils.instance.std_out.info(cls.format_input(msg), *args, **kwargs)

    @classmethod
    def error(cls, msg: Union[str, Dict], *args: List, **kwargs: Dict) -> None:
        print('error...')
        LoggerUtils.instance.std_err.error(cls.format_input(msg), *args, **kwargs)

    @classmethod
    def critical(cls, msg: Union[str, Dict], *args: List, **kwargs: Dict) -> None:
        LoggerUtils.instance.std_err.critical(cls.format_input(msg), *args, **kwargs)

    @classmethod
    def format_input(cls, msg: Union[str, Dict]) -> str:
        if type(msg) is dict:
            msg = json.dumps(msg)
        return msg