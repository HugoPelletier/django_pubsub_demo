"""
Consumer example

Pull messages front the queue and update the Redis key.
In the context of the PoC, the consumer only update the Product.Brand information.

@type: worker
"""
import json
import logging
import sys
from datetime import datetime
from typing import Dict

import boto3
from botocore.client import BaseClient
import redis

# Logger
logger = logging.getLogger('service-consumer')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False

r = redis.Redis(host='demo-redis', port=6379, db=0)
queue = 'http://localhost:4576/queue/service-consumer-queue'


def process() -> None:
    """
    Process messages from queue and store into redis

    :return: None
    """
    sqs_client = boto3.client(
        'sqs',
        aws_access_key_id='Foo',
        aws_secret_access_key='Bar',
        region_name='us-east-1',
        endpoint_url='http://aws-localstack:4576'
    )

    while True:
        try:
            messages = sqs_client.receive_message(QueueUrl=queue)

            if messages is not None and 'Messages' in messages.keys():
                for message in messages.get('Messages'):
                    receipt_handle = message.get('ReceiptHandle')
                    body = json.loads(message.get('Body', {}))

                    # store in redis
                    message = json.loads(body.get('Message'))
                    topic = message.get('metadata', {}).get('topic')
                    id = message.get('aggregate', {}).get('id')
                    redis_key = '{}:{}'.format(topic, id)

                    r.set(redis_key, json.dumps(message.get('aggregate')))
                    print('Redis key updated {}.'.format(redis_key))

                    sqs_client.delete_message(
                        QueueUrl=queue,
                        ReceiptHandle=receipt_handle
                    )

                    print('Message deleted {}.'.format(receipt_handle))

        except (TypeError, BaseException) as e:
            print(e)


def _build_log(body: Dict, response: Dict) -> Dict:
    """
    Format log

    :param body: dict
    :param response: dict
    :return: dict
    """
    log = {
        'app': 'service-consumer',
        'date': str(datetime.now()),
        'reqId': json.loads(body.get('Message')).get('metadata', {}).get(REQUEST_ID),
        'details': response
    }
    logger.info(log)


if __name__ == '__main__':
    try:
        process()
    except KeyboardInterrupt:
        logger.info('Consumer process manually stopped.')
