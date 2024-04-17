from adapter.local import Local
from config import Directory
from usecases.action import ActionWrite
from usecases.bucket import Bucket
from usecases.info import Information


class FileSynchronizer:

    def process(self, file_extension: str, file_path: str = ''):
        pass


class FileSynchronizerDirectories(FileSynchronizer):

    def __init__(self, synchronizer: FileSynchronizer, action: ActionWrite):
        self.synchronizer = synchronizer
        self.action = action

    def process(self, file_extension: str, file_path: str = ''):
        self.synchronizer.process(file_extension, file_path)

    def process_directories(self, directories: list[Directory]):
        for directory in directories:
            self.process(file_extension=directory.extension, file_path=directory.file_path)
        self.action.export()


class FileSynchronizerAtomic(FileSynchronizer):

    def __init__(self, bucket: Bucket, device: Local):
        self.bucket = bucket
        self.device = device

    def process(self, file_extension: str, file_path: str = ''):

        local_files: dict[str, Information] = self.device.find_files(file_extension=file_extension, file_path=file_path)

        s3_files: dict[str, str] = self.bucket.all(file_path=file_path)

        modified_files: dict[str, Information] = self._detect_modified_files(local_files=local_files, s3_files=s3_files)

        missing_files: set[Information] = self._find_missing_files(local_files=local_files, s3_files=s3_files)

        self._manage_files(modified_files=modified_files, missing_files=missing_files)

    def _manage_files(self, modified_files: dict[str, Information], missing_files: set[Information]):
        for filename, info in modified_files.items():
            self.bucket.upload(filename, info)
        for info in missing_files:
            self.bucket.remove(info)

    @staticmethod
    def _find_missing_files(local_files: dict[str, Information], s3_files: dict[str, str]) -> set[Information]:
        local_virtual_paths = {info.get_file_path() for info in local_files.values()}
        s3_missing_files = {key: value for key, value in s3_files.items() if key not in local_virtual_paths}
        return {Information(file_hash_old=value, file_path=key) for key, value in s3_missing_files.items()}

    @staticmethod
    def _detect_modified_files(local_files: dict[str, Information], s3_files: dict[str, str]) -> dict[str, Information]:
        modified_files: dict[str, Information] = {}
        for object_name, metadata in local_files.items():
            if metadata.get_file_path() not in s3_files:
                modified_files[object_name] = metadata
            elif not metadata.is_file_hash_match(s3_files[metadata.get_file_path()]):
                modified_files[object_name] = Information(file_hash=metadata.get_hash(),
                                                          file_path=metadata.get_file_path(),
                                                          file_hash_old=s3_files[metadata.get_file_path()])
        return modified_files
