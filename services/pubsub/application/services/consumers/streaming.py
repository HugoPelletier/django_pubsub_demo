import json
from typing import Dict

from application.services.consumers.base import BaseConsumer

from application.services.topic import TopicService

from configs.vars import AWS_SQS_STREAMING


class StreamingConsumerService(BaseConsumer):

    CONSUMER_QUEUE = AWS_SQS_STREAMING

    def __init__(self):
        super().__init__()
        self.service = TopicService()

    def distribute(self, message: str) -> Dict:
        """
        Distribute message to SNS for streaming

        :param message: str
        :return: dict
        """
        # extract topic from the metadata
        topic = json.loads(message).get('metadata', {}).get('topic')

        return self.service.publish(message, topic)
