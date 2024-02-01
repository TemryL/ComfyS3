import os
import boto3
from botocore.exceptions import NoCredentialsError

from dotenv import load_dotenv
load_dotenv()


class S3:
    def __init__(self, region, access_key, secret_key, bucket_name):
        self.region = region
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.s3_client = self.get_client()

    def get_client(self):
        if not all([self.region, self.access_key, self.secret_key, self.bucket_name]):
            raise ValueError("Missing required S3 environment variables")

        try:
            s3 = boto3.resource(
                service_name='s3',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key
            )
            return s3
        except Exception as e:
            raise RuntimeError(f"Failed to create S3 client: {e}")

    def get_files(self, prefix):
        try:
            bucket = self.s3_client.Bucket(self.bucket_name)
            files = [obj.key for obj in bucket.objects.filter(Prefix=prefix)]
            return files
        except Exception as e:
            raise RuntimeError(f"Failed to get files from S3: {e}")

    def download_file(self, s3_path, local_path):
        local_dir = os.path.dirname(local_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        try:
            bucket = self.s3_client.Bucket(self.bucket_name)
            bucket.download_file(s3_path, local_path)
            return local_path
        except NoCredentialsError:
            raise RuntimeError("Credentials not available or not valid.")
        except Exception as e:
            raise RuntimeError(f"Failed to download file from S3: {e}")

    def upload_file(self, local_path, s3_path):
        try:
            bucket = self.s3_client.Bucket(self.bucket_name)
            bucket.upload_file(local_path, s3_path)
            return s3_path
        except NoCredentialsError:
            raise RuntimeError("Credentials not available or not valid.")
        except Exception as e:
            raise RuntimeError(f"Failed to upload file to S3: {e}")


def get_s3_instance():
    s3_instance = S3(
        region=os.getenv("S3_REGION"),
        access_key=os.getenv("S3_ACCESS_KEY"),
        secret_key=os.getenv("S3_SECRET_KEY"),
        bucket_name=os.getenv("S3_BUCKET_NAME")
    )
    return s3_instance


# Example usage:
# s3_instance = get_s3_instance()
# s3_instance.upload_file(local_path="input/example_s3.jpeg", s3_path="input/example_s3.jpeg")
# s3_instance.download_file(s3_path="input/example_s3.jpeg", local_path="input/example_s3.jpeg")