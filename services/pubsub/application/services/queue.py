from functools import lru_cache
from typing import Optional, Dict, List

from botocore.exceptions import ClientError

from application.services.base import BaseService
from application.services.interface_base import InterfaceBaseService
from application.utils.logger import LoggerUtils

from application.exceptions.queue import QueueException

from application.models.enums.services import AWSServices
from configs.vars import AWS_SQS_URL, AWS_SQS_DELAY, AWS_SQS_MAX_MESSAGE


class QueueService(BaseService, InterfaceBaseService):

    def __init__(self):
        super().__init__(AWSServices.SQS.value, AWS_SQS_URL)

    def receive_message(self, queue: str, wait_time_sec: int = AWS_SQS_DELAY,
                        max_number_msg: int = AWS_SQS_MAX_MESSAGE) -> Optional[Dict]:

        return self.get_client().receive_message(
            QueueUrl=self._get_queue_url(queue),
            MaxNumberOfMessages=max_number_msg,
            WaitTimeSeconds=wait_time_sec
        )

    def delete_message(self, queue, receipt_handle: Optional[str] = None) -> None:
        """
        Delete message from the queue based on the ReceiptHandle

        :param queue: str
        :param receipt_handle: str
        :return: None
        """

        self.get_client().delete_message(
            QueueUrl=self._get_queue_url(queue),
            ReceiptHandle=receipt_handle
        )

    def create(self, name: str) -> None:
        """
        Create an SQS queue
        IMPORTANT: Make sure that your AWS have credential to create resource like an SQS bucket

        :return: None
        """

        try:
            self.get_client().create_queue(
                QueueName=name
            )
            LoggerUtils.info('Internal queue creation... \x1b[32mCOMPLETED')

            assert self.get_client().list_queues()

        except ClientError:
            raise QueueException('Unable to create queue `{}`'.format(name))


    def get_arn(self, target: str) -> str:
        """
        Get arn of a given queue name.
        Get list of all the queues and find the matching name to return the ARN.

        :param target: str
        :return: str
        """

        queues = self.get_client().list_queues().get('QueueUrls')

        if target not in list(map(lambda x: x.split('/')[-1], self._get_list_queues())):
            raise QueueException('Unable to find queue `{}`'.format(target))

        attributes = self.get_client().get_queue_attributes(
            QueueUrl=list(filter(lambda x: target == x.split('/')[-1], queues))[-1],
            AttributeNames=['QueueArn']
        )

        return attributes.get('Attributes', {}).get('QueueArn')

    @lru_cache(maxsize=32)
    def _get_queue_url(self, queue: str) -> str:
        """
        Get queue URL based on the queue name

        :param queue: str
        :return: str
        """
        queue_url = self.get_client().get_queue_url(QueueName=queue).get('QueueUrl')

        if not queue_url:
            raise QueueException('Unable to get the queue-url for `{}`'.format(queue))

        return queue_url

    @lru_cache(maxsize=32)
    def _get_list_queues(self) -> List:
        return self.get_client().list_queues().get('QueueUrls')
