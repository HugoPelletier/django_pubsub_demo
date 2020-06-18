import inspect
import os
import sys

# Add parent folder to the python path to be able to access "/application" and "/configs"
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from configs.vars import AWS_SQS_STREAMING, AWS_SQS_STORAGE
from application.services.queue import QueueService
from application.utils.logger import LoggerUtils

LoggerUtils.get_instance()
LoggerUtils.info('\x1b[33mCreate internal queues')

QueueService().create(AWS_SQS_STREAMING)
QueueService().create(AWS_SQS_STORAGE)

# ======================================================================================
# This is just to create queue in a fast way.
# This should be done with Terraform
QueueService().create('service-consumer-queue')
QueueService().create('boutique-consumer-queue')
