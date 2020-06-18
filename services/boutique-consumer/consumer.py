"""
Generic consumer

Based on the argument, this script will trigger the queue consumer.
There are 3 different consumers in the ms-pubsub structure:

1. publishing: has the responsibility to propagate the incoming messages to SNS
2. streaming: has the responsibility to send a copy of the incoming messages to the data-lake through Firehose
3. batch: has the responsibility to process batch requests.

@type: worker
"""
import json
import logging
import sys
from datetime import datetime
from typing import Dict

import boto3
from botocore.client import BaseClient
from firebase import firebase

# Logger
logger = logging.getLogger('boutique-consumr')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False

# SQS Queue
queue = 'http://localhost:4576/queue/boutique-consumer-queue'

# Firebase
firebase_connector = firebase.FirebaseApplication('https://ruelala-dev.firebaseio.com', None)

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

                    # store in Firebase
                    message = json.loads(body.get('Message'))
                    topic = message.get('metadata', {}).get('topic')



                    #firebase.post('/boutiquetest/innoday06182020', data)

                    print('topic == {}'.format(topic))
                    print('message ==')
                    print(message)

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
        'reqId': json.loads(body.get('Message')).get('metadata', {}).get('x-request-id'),
        'details': response
    }
    logger.info(log)


if __name__ == '__main__':
    try:
        process()
    except KeyboardInterrupt:
        logger.info('Consumer process manually stopped.')
