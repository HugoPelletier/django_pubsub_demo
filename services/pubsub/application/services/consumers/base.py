import abc
from typing import Dict, Optional

from application.services.queue import QueueService
from configs.vars import AWS_SQS_DELAY, AWS_SQS_MAX_MESSAGE


class BaseConsumer:

    def __init__(self):
        self.queue = QueueService()

    @abc.abstractmethod
    def distribute(self, message: Dict) -> None:
        """This method needs to be implemented by classes using this interface"""

    def delete(self, id: str) -> None:
        """
        Delete message in the queue

        :param id: str ReceiptHandle id
        :return: None
        """

        self.queue.delete_message(self.CONSUMER_QUEUE, receipt_handle=id)

    def pull_messages(self, delay: int = AWS_SQS_DELAY,
                      number_of_messages: int = AWS_SQS_MAX_MESSAGE) -> Optional[Dict]:
        """
        Pull messages from the queue of the consumer service

        :param delay: int Number of seconds to hold the pull on the queue
        :param number_of_messages: int Number of messages to retrieve at each pull
        :return: dict
        """
        return self.queue.receive_message(self.CONSUMER_QUEUE, wait_time_sec=delay, max_number_msg=number_of_messages)
