import os
from ..client_s3 import get_s3_instance
S3_INSTANCE = get_s3_instance()


class UploadFileS3:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "local_path": ("STRING", {"default": "input/example.png"}),
                "s3_folder": ("STRING", {"default": "output"}),
                "delete_local": (["false", "true"],),
            }
        }

    CATEGORY = "ComfyS3"
    INPUT_NODE = True
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("s3_paths",)
    FUNCTION = "upload_file_s3"

    def upload_file_s3(self, local_path, s3_folder, delete_local):
        if isinstance(local_path, str):
            local_path = [local_path]
        s3_paths = []
        for path in local_path:
            s3_path = os.path.join(s3_folder, os.path.basename(path))
            file_path = S3_INSTANCE.upload_file(path, s3_path)
            s3_paths.append(file_path)
            if delete_local == "true":
                os.remove(path)
                print(f"Deleted file at {path}")
        print(f"Uploaded file to S3 at {s3_path}")
        return { "ui": { "s3_paths": s3_paths },  "result": (s3_paths,) }