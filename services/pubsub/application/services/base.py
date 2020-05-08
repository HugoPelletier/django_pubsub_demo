import boto3
from botocore.client import BaseClient

from application.exceptions.service import ServiceException
from configs.vars import AWS_SECRET_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY


class BaseService:

    def __init__(self, client: str, url: str = None) -> None:
        self._client: BaseClient = self.set_client(client, url=url)

    def set_client(self, client: str, url: str = None) -> BaseClient:
        """
        Set boto3 client

        :param client: str
        :param url: str
        :return: BaseClient
        """
        if not url:
            raise ServiceException('url is mandatory in development mode')

        client = boto3.client(
            client,
            aws_access_key_id=AWS_SECRET_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION,
            endpoint_url=url
        )

        return client

    def get_client(self) -> BaseClient:
        """
        Return botocore client class

        :return: BaseClient
        """

        return self._client

