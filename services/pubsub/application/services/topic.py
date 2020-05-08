import json
from functools import lru_cache
from typing import Dict, Union, Optional

from botocore.exceptions import ClientError

from application.services.base import BaseService
from application.services.interface_base import InterfaceBaseService
from application.exceptions.topic import TopicException

from application.services.queue import QueueService

from application.models.enums.services import AWSServices

from application.models.enums.protocol import SnsProtocol

from configs.vars import AWS_SNS_URL, REQUEST_ID


class TopicService(BaseService, InterfaceBaseService):

    def __init__(self):
        super().__init__(AWSServices.SNS.value, AWS_SNS_URL)

    def publish(self, message: Union[Dict, str], topic: str) -> Dict:
        """
        Publish message to the internal pubsub queue

        :param message: dict or str
        :param topic: str Topic
        :return: dict
        """
        if isinstance(message, (dict)):
            message = json.dumps(message)

        try:
            output = self._client.publish(
                TopicArn=self._get_topic_arn(topic),
                Message=message
            )

            return output.get('MessageId')
        except ClientError:
            raise TopicException('An error occurred (500) when calling `PutRecord operation`.\n'
                                 'Message Id: {message_id}\n'
                                 'Topic arn: {topic}'.format(message_id=req.get_header(REQUEST_ID),
                                                             topic=self._get_topic_arn(topic)))

    def create(self, topic: str) -> str:
        """
        Create topic and return the ARN
        IMPORTANT: Make sure that your AWS have credential to create topic

        :param topic: str
        :return: None
        """

        try:
            result = self._client.create_topic(Name=TopicService.transform_topic_name(topic))
            if result and 'TopicArn' in result.keys():
                return result.get('TopicArn')

            raise TopicException('Unable to create topic for {}'.format(topic))
        except ClientError:
            raise TopicException('Client Error: unable to create topics from AWS.')

    def subscriptions(self, protocol: str, target: str, topic: str) -> str:
        """
        Found the target based on the protocol and try to create a subscriptions for this topic

        :param protocol: str
        :param target: str
        :param topic: str
        :return: str
        """

        # Get ARN of the protocol target
        protocol_arn = self._get_protocol_target_arn(protocol, target)

        # Get topic ARN
        topic_arn = self._get_topic_arn(topic)

        try:
            return self._client.subscribe(
                TopicArn=topic_arn,
                Protocol=SnsProtocol.SQS.value,
                Endpoint=protocol_arn,
                ReturnSubscriptionArn=True
            )
        except ClientError:
            raise TopicException('Unable to create subscription between {} - {} and {}'.format(protocol, target, topic))

    def _get_topic_arn(self, topic: str) -> Optional[str]:
        """
        Get topic arn

        :param topic: str
        :return: str
        """

        topics = self._load_topics()
        if topic in topics.keys():
            return topics.get(topic)

        raise TopicException('Unable to find ARN for topic `{}`'.format(topic))

    @lru_cache(maxsize=32)
    def _load_topics(self, token: str = None, list_topics: Dict = dict()) -> Dict:
        """
        Load topics ARN from AWS

        :param token: str
        :param list_topics: list
        :return: dict
        """
        try:
            args = {}
            if token is not None:
                args = {'NextToken': token}

            result = self._client.list_topics(**args)

            if result:
                for topic in result.get('Topics'):
                    split = topic.get('TopicArn').split(':')
                    name = self.transform_topic_name(split[-1], True)
                    arn = ':'.join(split)
                    list_topics[name] = arn

            if 'NextToken' in result.keys() and result.get('NextToken') != '' and result.get('NextToken') is not None:
                self._load_topics(result.get('NextToken'), list_topics)

            return list_topics
        except ClientError:
            raise TopicException('Unable to retrieve topics from AWS.')

    def _get_protocol_target_arn(self, protocol, target) -> str:
        """
        Get the ARN of target based on the protocol

        :param protocol: str
        :param target: str
        :return: str
        """

        if protocol == SnsProtocol.SQS.value:
            return QueueService().get_arn(target)
        else:
            raise TopicException('Only SQS is supported for the moment.')

    @staticmethod
    def transform_topic_name(topic_name: str, reverse=False) -> str:
        """
        Take a given given and transform it into another format

        :param topic_name: str
        :param reverse: bool
        :return: str
        """
        if reverse:
            return topic_name.replace('_', '.')

        return topic_name.replace('.', '_')
