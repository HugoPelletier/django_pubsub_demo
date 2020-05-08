import inspect
import os
import sys

# Add parent folder to the python path to be able to access "/application" and "/configs"
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from application.utils.logger import LoggerUtils

LoggerUtils.get_instance()
LoggerUtils.info('\x1b[33mCreate internal stream')
