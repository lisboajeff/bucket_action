import argparse
import os
import re

import boto3

from adapter.s3 import S3
from summary import Summary, SummaryVisitor
from usecases.action import Action, ActionInsert
from usecases.bucket import Bucket, BucketActionProxy
from usecases.bucket_planning import BucketPlanning


class Directory:

    def __init__(self, file_path: str, extension: str):
        self.file_path = file_path
        self.extension = extension


class Config:

    def __init__(self):
        parser = argparse.ArgumentParser(description="Arguments")
        parser.add_argument('type', type=str, help="Planning or Apply")
        parser.add_argument('pairs', type=str, help="A comma-separated list of folder=extension pairs.")
        arguments = parser.parse_args()
        self.pairs: str = arguments.pairs
        self.types: list[str] = ['apply', 'planning']
        self.type: str = arguments.type
        if self.type not in self.types:
            raise ValueError(f"Type is invalid: {type}")

    def get_directories(self) -> list[Directory]:
        regex = re.compile('^([a-zA-Z0-9_]+=[a-zA-Z0-9_]+)(,[a-zA-Z0-9_]+=[a-zA-Z0-9_]+)*$')
        if not regex.match(self.pairs):
            raise ValueError(f"Input({self.pairs}) string is invalid.\n Pattern is : {regex.pattern}")
        return [Directory(pair.split('=')[0], pair.split('=')[1]) for pair in self.pairs.split(',')]

    @staticmethod
    def _get_aws_region():
        return "".join(os.getenv('AWS_REGION'))

    @staticmethod
    def _get_bucket_name():
        return os.getenv('BUCKET_NAME')

    @staticmethod
    def get_description():
        return os.getenv('DESCRIPTION')

    @staticmethod
    def get_base_path():
        return os.getenv('BASE_PATH')

    def action(self, filename: str) -> Action:

        if self.type == 'planning':
            report_without_actions = 'no files to be added or removed in planning'
            text = 'The report presents the change planning'
            uploaded_message = 'Upload plan'
            remove_message = 'Removal plan'
        else:
            report_without_actions = 'No file was added or removed.'
            text = 'The report presents the changes that were synchronized'
            uploaded_message = 'Uploaded'
            remove_message = 'Removed'

        class SummaryVisitorImpl(SummaryVisitor):

            def uploaded_message(self) -> str:
                return uploaded_message

            def remove_message(self) -> str:
                return remove_message

            def report_without_actions(self) -> str:
                return report_without_actions

            def title(self) -> str:
                return text

        return Summary(self.get_description(), filename=filename, visitor=SummaryVisitorImpl())

    def create_bucket_instance(self, action: ActionInsert) -> Bucket:

        s3: S3 = S3(s3_client=boto3.client('s3', region_name=(self._get_aws_region())),
                    bucket_name=self._get_bucket_name())

        if self.type == 'planning':
            return BucketActionProxy(bucket=BucketPlanning(bucket=s3), action=action)

        return BucketActionProxy(bucket=s3, action=action)
