from application.services.base import BaseService
from application.services.interface_base import InterfaceBaseService
from application.utils.logger import LoggerUtils

from application.models.enums.services import AWSServices
from configs.vars import AWS_S3_URL, AWS_REGION


class BucketService(BaseService, InterfaceBaseService):

    def __init__(self):
        super().__init__(AWSServices.S3.value, AWS_S3_URL)

    def create(self, name: str) -> None:
        """
        Create S3 bucket
        IMPORTANT: Make sure that your AWS have credential to create resource like an S3 bucket

        :return: None
        """

        try:
            self.get_client().create_bucket(
                Bucket=name,
                CreateBucketConfiguration={'LocationConstraint': AWS_REGION},
                ObjectLockEnabledForBucket=False
            )

            assert self.get_client().list_buckets() is not None
            LoggerUtils.info('S3 bucket(s) created... \x1b[32mCOMPLETED')

        except self.get_client().exceptions.BucketAlreadyExists:
            pass
