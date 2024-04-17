from adapter.local import Local
from config import Config
from src.usecases.action import Action
from src.usecases.bucket import Bucket
from src.usecases.synchronize import FileSynchronizerDirectories
from usecases.synchronize import FileSynchronizerAtomic


def main():
    config: Config = Config()

    action: Action = config.action(filename="s3_sync_report.md")

    bucket: Bucket = config.create_bucket_instance(action=action)

    device: Local = Local(base_path=config.get_base_path())

    file_synchronizer_directories: FileSynchronizerDirectories = FileSynchronizerDirectories(
        synchronizer=(FileSynchronizerAtomic(bucket=bucket, device=device)), action=action)

    file_synchronizer_directories.process_directories(config.get_directories())


if __name__ == "__main__":
    main()
