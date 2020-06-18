import inspect
import os
import sys

# Add parent folder to the python path to be able to access "/application" and "/configs"
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from application.services.topic import TopicService
from application.utils.logger import LoggerUtils
from configs.vars import AWS_SNS_TOPIC

LoggerUtils.get_instance()
LoggerUtils.info('\x1b[33mCreate internal topic')

TopicService().create(AWS_SNS_TOPIC)

# ======================================================================================
# This is just to create topic in a fast way.
# This should be done with Terraform
TopicService().create('Products.Brand')
TopicService().create('Products.Category')
TopicService().create('Products.Product')
TopicService().create('Storemanager.Boutique')
