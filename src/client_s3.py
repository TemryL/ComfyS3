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
        self.input_dir = os.getenv("S3_INPUT_DIR")
        self.output_dir = os.getenv("S3_OUTPUT_DIR")
        if not self.does_folder_exist(self.input_dir):
            self.create_folder(self.output_dir)
        if not self.does_folder_exist(self.output_dir):
            self.create_folder(self.output_dir)

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
        if self.does_folder_exist(prefix):
            try:
                bucket = self.s3_client.Bucket(self.bucket_name)
                files = [obj.key for obj in bucket.objects.filter(Prefix=prefix)]
                files = [f.replace(prefix, "") for f in files]
                return files
            except Exception as e:
                raise RuntimeError(f"Failed to get files from S3: {e}")
        else:
            return []
    
    def does_folder_exist(self, folder_name):
        try:
            bucket = self.s3_client.Bucket(self.bucket_name)
            response = bucket.objects.filter(Prefix=folder_name)
            return any(obj.key.startswith(folder_name) for obj in response)
        except Exception as e:
            raise RuntimeError(f"Failed to check if folder exists in S3: {e}")
    
    def create_folder(self, folder_name):
        try:
            bucket = self.s3_client.Bucket(self.bucket_name)
            bucket.put_object(Key=f"{folder_name}/")
        except Exception as e:
            raise RuntimeError(f"Failed to create folder in S3: {e}")
    
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
    
    def get_save_path(self, filename_prefix, image_width=0, image_height=0):
        def map_filename(filename):
            prefix_len = len(os.path.basename(filename_prefix))
            prefix = filename[:prefix_len + 1]
            try:
                digits = int(filename[prefix_len + 1:].split('_')[0])
            except:
                digits = 0
            return (digits, prefix)

        def compute_vars(input, image_width, image_height):
            input = input.replace("%width%", str(image_width))
            input = input.replace("%height%", str(image_height))
            return input

        filename_prefix = compute_vars(filename_prefix, image_width, image_height)
        subfolder = os.path.dirname(os.path.normpath(filename_prefix))
        filename = os.path.basename(os.path.normpath(filename_prefix))
        
        full_output_folder_s3 = os.path.join(self.output_dir, subfolder)
        
        # Check if the output folder exists, create it if it doesn't
        if not self.does_folder_exist(full_output_folder_s3):
            self.create_folder(full_output_folder_s3)

        try:
            # Continue with the counter calculation
            files = self.get_files(full_output_folder_s3)
            counter = max(
                filter(
                    lambda a: a[1][:-1] == filename and a[1][-1] == "_",
                    map(map_filename, files)
                )
            )[0] + 1
        except (ValueError, KeyError):
            counter = 1
        
        return full_output_folder_s3, filename, counter, subfolder, filename_prefix


def get_s3_instance():
    s3_instance = S3(
        region=os.getenv("S3_REGION"),
        access_key=os.getenv("S3_ACCESS_KEY"),
        secret_key=os.getenv("S3_SECRET_KEY"),
        bucket_name=os.getenv("S3_BUCKET_NAME")
    )
    return s3_instance