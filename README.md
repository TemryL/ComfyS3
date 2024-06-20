# ComfyS3: Amazon S3 Integration for ComfyUI 
ComfyS3 seamlessly integrates with [Amazon S3](https://aws.amazon.com/en/s3/) in [ComfyUI](https://github.com/comfyanonymous/ComfyUI). This open-source project provides custom nodes for effortless loading and saving of images, videos, and checkpoint models directly from S3 buckets within the ComfyUI graph interface.

## Installation

### Using ComfyUI Manager:

- Look for ```ComfyS3```, and be sure the author is ```TemryL```. Install it.

### Manually:
- Clone this repo into `custom_nodes` folder in ComfyUI.

### Define S3 Config
Create `.env` file in ComfyS3 root folder with the following variables:

```bash 
S3_REGION = "..."
S3_ACCESS_KEY = "..."
S3_SECRET_KEY = "..."
S3_BUCKET_NAME = "..."
S3_INPUT_DIR = "..."
S3_OUTPUT_DIR = "..."
```

### Optional S3 Config Variables
- ```S3_ENDPOINT_URL``` allows the useage of a AWS Private Link or Other S3 Compatible Storage Solutions

## Available Features
ComfyUI nodes to:
- [x] standalone download/upload file from/to Amazon S3
- [x] load/save image from/to Amazon S3 buckets
- [x] save VHS (VideoHelperSuite) video files to Amazon S3 buckets
- [x] install ComfyS3 from [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
- [ ] load checkpoints from Amazon S3 buckets
- [ ] load video from Amazon S3 buckets

## Credits
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)
