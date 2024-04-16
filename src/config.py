import argparse
import os
import re


class Directory:

    def __init__(self, file_path: str, extension: str):
        self.file_path = file_path
        self.extension = extension


class Config:

    def __init__(self):
        parser = argparse.ArgumentParser(description="Arguments")
        parser.add_argument('pairs', type=str, help="A comma-separated list of folder=extension pairs.")
        arguments = parser.parse_args()
        self.pairs: str = arguments.pairs

    def get_directories(self) -> list[Directory]:
        regex = re.compile('^([a-zA-Z0-9_]+=[a-zA-Z0-9_]+)(,[a-zA-Z0-9_]+=[a-zA-Z0-9_]+)*$')
        if not regex.match(self.pairs):
            raise ValueError(f"Input({self.pairs}) string is invalid.\n Pattern is : {regex.pattern}")
        return [Directory(pair.split('=')[0], pair.split('=')[1]) for pair in self.pairs.split(',')]

    @staticmethod
    def get_aws_region():
        return "".join(os.getenv('AWS_REGION'))

    @staticmethod
    def get_bucket_name():
        return os.getenv('BUCKET_NAME')

    @staticmethod
    def get_description():
        return os.getenv('DESCRIPTION')

    @staticmethod
    def get_base_path():
        return os.getenv('BASE_PATH')
