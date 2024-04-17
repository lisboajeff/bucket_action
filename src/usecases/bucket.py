from src.usecases.action import ActionInsert
from src.usecases.info import Information


class Bucket:

    def all(self, file_path: str) -> dict[str, str]:
        pass

    def upload(self, filename: str, info: Information):
        pass

    def remove(self, info: Information):
        pass


class BucketActionProxy(Bucket):
    def __init__(self, bucket: Bucket, action: ActionInsert):
        self.bucket = bucket
        self.action = action

    def all(self, file_path: str) -> dict[str, str]:
        return self.bucket.all(file_path)

    def upload(self, filename: str, info: Information):
        self.bucket.upload(filename, info)
        self.action.insert_uploaded(info)

    def remove(self, info: Information):
        self.bucket.remove(info)
        self.action.insert_removed(info)
