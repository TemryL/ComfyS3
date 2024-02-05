from ..client_s3 import get_s3_instance
S3_INSTANCE = get_s3_instance()


class UploadFileS3:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "local_path": ("STRING", {"default": "input/example.png"}),
                "s3_path": ("STRING", {"default": "output/example.png"}),
            }
        }

    CATEGORY = "ComfyS3"
    INPUT_NODE = True
    OUTPUT_NODE = True
    RETURN_TYPES = ()
    FUNCTION = "upload_file_s3"

    def upload_file_s3(self, local_path, s3_path):
        S3_INSTANCE.upload_file(local_path, s3_path)
        print(f"Uploaded file to S3 at {s3_path}")
        return {}