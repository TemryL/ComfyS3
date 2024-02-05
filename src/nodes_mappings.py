from .nodes.load_image_s3 import LoadImageS3
from .nodes.save_image_s3 import SaveImageS3
from .nodes.save_video_files_s3 import SaveVideoFilesS3
from .nodes.download_file_s3 import DownloadFileS3
from .nodes.upload_file_s3 import UploadFileS3


NODE_CLASS_MAPPINGS = {
    "LoadImageS3": LoadImageS3,
    "SaveImageS3": SaveImageS3,
    "SaveVideoFilesS3": SaveVideoFilesS3,
    "DownloadFileS3": DownloadFileS3,
    "UploadFileS3": UploadFileS3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageS3": "Load Image from S3",
    "SaveImageS3": "Save Image to S3",
    "SaveVideoFilesS3": "Save Video Files to S3",
    "DownloadFileS3": "Download File from S3",
    "UploadFileS3": "Upload File to S3"
}