import json
from typing import Dict

from falcon import Request

from application.services.topic import TopicService

from configs.vars import REQUEST_ID, AWS_SNS_TOPIC


class MessageService:

    def validate(self, req: Request) -> None:
        """
        Validate message input
        :param req: Request
        :return: None
        """

        self._validate_size(req)
        self._validate_topic(req)
        self._validate_version(req)
        self._validate_content(req)

    def publish(self, req: Request) -> Dict:
        """
        Send request to SNS and return response

        :param req: Request
        :return: dict
        """

        # Add x-request-id to the metadata
        msg = req.json
        metadata = msg.get('metadata')
        metadata[REQUEST_ID] = req._params.get(REQUEST_ID)
        msg['metadata'] = metadata
        req.json = msg

        # size validation
        self._validate_size(req)

        return TopicService().publish(req.json, AWS_SNS_TOPIC)

    def _validate_topic(self, req: Request) -> None:
        """
        Validate if the topic is valid.
        If not, throw a TopicException

        @todo: implement this method
        :param req: Request
        :return: None
        """
        pass

    def _validate_version(self, req: Request) -> None:
        """
        Validate if the content of the message match the expected version
        If not, throw a TopicException

        @todo: implement this method
        :param req: Request
        :return: None
        """
        pass

    def _validate_content(self, req: Request) -> None:
        """
        Validate if the content of the message match the expected structure
        If not, throw a TopicException

        @todo: implement this method
        :param req: Request
        :return: None
        """
        pass

    def _validate_size(self, req):
        """
        Validate size of the message.
        Limit 256KB

        @todo: implement this method
        :param req: Request
        :return: None
        """
        pass
