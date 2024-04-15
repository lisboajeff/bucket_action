import boto3

from adapter.local import Local
from adapter.s3 import S3
from config import Config
from summary import Summary
from usecases.synchronize import FileSynchronizer


def main():
    config: Config = Config()

    summary: Summary = Summary(config.get_description())

    s3: S3 = S3(s3_client=boto3.client('s3', region_name=(config.get_aws_region())),
                bucket_name=config.get_bucket_name(),
                action=summary)

    device: Local = Local(base_path=config.get_base_path())

    file_synchronizer: FileSynchronizer = FileSynchronizer(s3=s3, device=device)

    for directory in config.get_directories():
        file_synchronizer.process(file_extension=directory.extension, file_path=directory.file_path)

    summary.write_text("s3_sync_report.md")


if __name__ == "__main__":
    main()
