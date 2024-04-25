import hashlib
import os

from usecases.bucket.directory import Directory
from usecases.info import Information


class Local:

    def __init__(self, base_path: str):
        self.base_path = base_path

    @staticmethod
    def _determine_sha256_hash(full_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(full_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def find_files(self, directory: Directory) -> dict[str, Information]:
        abs_path: str = os.path.join(self.base_path, directory.file_path)
        files_with_hash: dict[str, Information] = {}
        if not os.path.exists(abs_path) or not os.listdir(abs_path):
            return files_with_hash
        for f in os.listdir(abs_path):
            file_abs_path: str = os.path.join(abs_path, f)
            if f.endswith(directory.extension) and os.path.isfile(file_abs_path):
                file_hash = self._determine_sha256_hash(file_abs_path)
                files_with_hash[file_abs_path] = (
                    Information(file_hash=file_hash,
                                file_path=f"{directory.file_path}/{os.path.basename(file_abs_path)}")
                )
        return files_with_hash
