from typing import Dict

from application.services.consumers.base import BaseConsumer


class StorageConsumerService(BaseConsumer):

    def pull_messages(self, message: Dict) -> None:
        pass
