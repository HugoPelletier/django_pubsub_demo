from enum import Enum


class SnsProtocol(Enum):
    SQS = 'sqs'
    LAMBDA = 'lambda'
