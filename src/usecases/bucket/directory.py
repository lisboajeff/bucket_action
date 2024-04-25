from usecases.bucket.bucket import Bucket
from usecases.info import Information


class Directory:

    def __init__(self, virtual_path: str, file_path: str, extension: str):
        self.file_path = file_path
        self.extension = extension
        self.virtual_path = virtual_path

    def find_files_bucket(self, bucket: Bucket) -> dict[str, str]:
        bucket_files: dict[str, str] = bucket.all(file_path=self._abs_file_path())
        return {name.replace(f'{self.virtual_path}/', ''): file_hash for name, file_hash in bucket_files.items()}

    def manage_files(self, bucket: Bucket, modified_files: dict[str, Information], missing_files: set[Information]):
        for filename, info in modified_files.items():
            bucket.upload(filename=filename, info=self._create_information(info=info))
        for info in missing_files:
            bucket.remove(info=self._create_information(info=info))

    def _abs_file_path(self, file_path=None) -> str:
        return f'{self.virtual_path}/{self.file_path if file_path is None else file_path}'

    def _create_information(self, info):
        return Information(file_path=self._abs_file_path(info.get_file_path()),
                           file_hash=info.get_hash(),
                           file_hash_old=info.get_old_hash())
