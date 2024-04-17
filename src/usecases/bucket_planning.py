from src.usecases.bucket import Bucket
from src.usecases.info import Information


class BucketPlanning(Bucket):

    def __init__(self, bucket: Bucket):
        self.bucket = bucket

    def all(self, file_path: str) -> dict[str, str]:
        return self.bucket.all(file_path)

    def upload(self, filename: str, info: Information):
        super().upload(filename, info)

    def remove(self, info: Information):
        super().remove(info)
