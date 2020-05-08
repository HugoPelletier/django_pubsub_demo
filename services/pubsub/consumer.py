"""
Generic consumer

Based on the argument, this script will trigger the queue consumer.
There are 3 different consumers in the ms-pubsub structure:

1. publishing: has the responsibility to propagate the incoming messages to SNS
2. streaming: has the responsibility to send a copy of the incoming messages to the data-lake through Firehose
3. batch: has the responsibility to process batch requests.

@type: worker
"""
import argparse
import json
from datetime import datetime
from typing import Dict

from application.models.enums.consumer import ConsumerEnum

from application.services.consumers.storage import StorageConsumerService

from application.services.consumers.base import BaseConsumer

from application.services.consumers.streaming import StreamingConsumerService

from application.exceptions.consumer import ConsumerException
from application.utils.logger import LoggerUtils


# Logger instance
from configs.vars import REQUEST_ID

LoggerUtils.get_instance()


def get_service(consumer: str) -> BaseConsumer:
    """
    Based on the consumer, return instance of the service.

    :param consumer: str
    :return: StreamingConsumerService, StorageConsumerService
    """

    if consumer == ConsumerEnum.STREAMING.value:
        return StreamingConsumerService()
    if consumer == ConsumerEnum.STORAGE.value:
        return StorageConsumerService()

    raise ConsumerException('Invalid consumer type ({})'.format(consumer))


def process(service: BaseConsumer) -> None:
    """
    Process messages from queue define in the service

    :param service: BaseConsumer
    :return: None
    """

    while True:
        try:
            messages = service.pull_messages()

            if messages is not None and 'Messages' in messages.keys():
                LoggerUtils.debug('Total message pull :: {}'.format(len(messages.get('Messages'))))
                for message in messages.get('Messages'):
                    body = json.loads(message.get('Body', {}))

                    response = service.distribute(body.get('Message'))
                    _build_log(service, body, response)
                    service.delete(message.get('ReceiptHandle'))

        except (TypeError, BaseException) as e:
            LoggerUtils.error(str(e))


def _build_log(service: BaseConsumer, body: Dict, response: Dict) -> Dict:
    """
    Format log

    :param service: BaseConsumer
    :param body: dict
    :param response: dict
    :return: dict
    """
    log = {
            'app': 'pubsub-consumer',
            'date': str(datetime.now()),
            'reqId': json.loads(body.get('Message')).get('metadata', {}).get(REQUEST_ID),
            'service': service.__class__.__name__,
            'details': response
        }
    LoggerUtils.info(log)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Consumer generator')
    parser.add_argument('--consumer', choices=[ConsumerEnum.STORAGE.value, ConsumerEnum.STREAMING.value],
                        help='consumer type')
    args = parser.parse_args()
    service = get_service(args.consumer)

    try:
        process(service)
    except KeyboardInterrupt:
        LoggerUtils.info('Consumer process manually stopped.')
