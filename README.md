# ComfyS3: S3 Integration for ComfyUI 
ComfyS3 seamlessly integrates with Amazon S3 in ComfyUI. This open-source project provides custom nodes for effortless loading and saving of images, videos, and checkpoint models directly from S3 buckets within the ComfyUI graph interface.


# Define S3 config
Create `.env` file in ComfyS3 root folder with the following variables:

```bash 
S3_REGION = "..."
S3_ACCESS_KEY = "..."
S3_SECRET_KEY = "..."
S3_BUCKET_NAME = "..."
S3_INPUT_DIR = "..."
S3_OUTPUT_DIR = "..."
```