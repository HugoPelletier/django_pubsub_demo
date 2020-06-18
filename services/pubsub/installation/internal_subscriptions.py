import inspect
import os
import sys

# Add parent folder to the python path to be able to access "/application" and "/configs"
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from application.models.enums.protocol import SnsProtocol
from application.services.topic import TopicService
from application.utils.logger import LoggerUtils
from configs.vars import AWS_SNS_TOPIC, AWS_SQS_STREAMING, AWS_SQS_STORAGE

LoggerUtils.get_instance()
LoggerUtils.info('\x1b[33mCreate subscriptions')

# Queue to redirect to SNS for streaming
TopicService().subscriptions(SnsProtocol.SQS.value, AWS_SQS_STREAMING, AWS_SNS_TOPIC)
LoggerUtils.info('\x1b[33mSubscriptions {} - {} and {} completed'.format(SnsProtocol.SQS.value,
                                                                         AWS_SQS_STREAMING, AWS_SNS_TOPIC))

# Queue to send to the storage
TopicService().subscriptions(SnsProtocol.SQS.value, AWS_SQS_STORAGE, AWS_SNS_TOPIC)
LoggerUtils.info('\x1b[33mSubscriptions {} - {} and {} completed'.format(SnsProtocol.SQS.value,
                                                                         AWS_SQS_STORAGE, AWS_SNS_TOPIC))


# ======================================================================================
# This is just to create subscriptions in a fast way.
# This should be done with Terraform
TopicService().subscriptions(SnsProtocol.SQS.value, 'service-consumer-queue', 'Products.Brand')
TopicService().subscriptions(SnsProtocol.SQS.value, 'service-consumer-queue', 'Products.Category')
TopicService().subscriptions(SnsProtocol.SQS.value, 'service-consumer-queue', 'Products.Product')
TopicService().subscriptions(SnsProtocol.SQS.value, 'boutique-consumer-queue', 'Storemanager.Boutique')
