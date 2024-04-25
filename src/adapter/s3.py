from botocore.client import BaseClient

from usecases.bucket.bucket import Bucket
from usecases.info import Information


class S3(Bucket):

    def __init__(self, s3_client: BaseClient, bucket_name: str):
        self.s3_client: BaseClient = s3_client
        self.bucket_name: str = bucket_name

    def all(self, file_path: str) -> dict[str, str]:
        objects_with_hash: dict[str, str] = {}
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=file_path)
        if 'Contents' in response:
            for obj in response['Contents']:
                obj_key = obj['Key']
                if not obj_key.endswith('/'):
                    meta = self.s3_client.head_object(Bucket=self.bucket_name, Key=obj_key)
                    obj_hash = meta['Metadata'].get('hash', '')
                    objects_with_hash[obj_key] = obj_hash
        return objects_with_hash

    def upload(self, filename: str, info: Information):
        try:
            key: str = info.get_file_path()
            with open(filename, 'rb') as f:
                self.s3_client.upload_fileobj(
                    Fileobj=f,
                    Bucket=self.bucket_name,
                    Key=key,
                    ExtraArgs={'Metadata': {'hash': info.get_hash()}}
                )
            print(f"Uploaded {filename} to s3://{self.bucket_name}/{key}")
        except Exception as e:
            self._log_action_error("upload", filename, e)

    def remove(self, info: Information):
        key: str = info.get_file_path()
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            print(f"Removed {key} from s3://{self.bucket_name}/{key}")
        except Exception as e:
            self._log_action_error("remove", key, e)

    @staticmethod
    def _log_action_error(action: str, filename: str, error: Exception):
        print(f"Failed to {action} {filename}: {error}")
