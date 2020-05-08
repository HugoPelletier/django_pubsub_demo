import os

from application.models.enums.environment import EnvironmentEnum

# general
REQUEST_ID = 'x-request-id'

# environment
ENV = os.getenv('ENV', EnvironmentEnum.DEV.value)

# AWS
AWS_SECRET_KEY_ID = os.getenv('AWS_SECRET_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRETE_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

AWS_FIREHOSE_URL = os.getenv('AWS_FIREHOSE_URL', 'https://firehose.us-west-2.amazonaws.com')
AWS_FIREHOSE_STREAM = os.getenv('AWS_FIREHOSE_STREAM', 'pubsub-dev')

AWS_SQS_URL = os.getenv('AWS_SQS_URL', 'https://sqs.us-west-2.amazonaws.com')
AWS_SQS_STREAMING = os.getenv('AWS_SQS_QUEUE', 'pubsub-streaming-dev')
AWS_SQS_STORAGE = os.getenv('AWS_SQS_QUEUE', 'pubsub-storage-dev')
AWS_SQS_DELAY = int(os.getenv('AWS_SQS_DELAY', 20))
AWS_SQS_MAX_MESSAGE = int(os.getenv('AWS_SQS_MAX_MESSAGE', 10))

AWS_S3_URL = os.getenv('AWS_S3_URL', 'https://s3.us-west-2.amazonaws.com')
AWS_S3_NAME = os.getenv('AWS_S3_NAME', 'pubsub')

AWS_SNS_URL = os.getenv('AWS_SNS_URL', 'https://sns.us-west-2.amazonaws.com')
AWS_SNS_TOPIC = os.getenv('AWS_SNS_TOPIC', 'Pubsub.Message')

