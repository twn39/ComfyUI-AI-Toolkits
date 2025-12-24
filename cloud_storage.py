import io
import boto3
from .utils import tensor_to_pil_image


class CloudflareR2:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", ),
                "bucket": ("STRING", {"multiline": False}),
                "key_name": ("STRING", {"multiline": False}),
                "account_id": ("STRING", {"multiline": False}),
                "access_key_id": ("STRING", {"multiline": False}),
                "secret_access_key": ("STRING", {"multiline": False}),
                "image_format": (["PNG", "JPG", "WEBP"], {"default": "PNG"})
            },
            "optional": {
                "public_domain": ("STRING", {"multiline": False, "default": None, "placeholder": "https://"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("url",)
    FUNCTION = "put_image_to_r2"

    CATEGORY = "AIToolkits/CloudStorage"

    @staticmethod
    def put_image_to_r2(image, bucket, key_name, account_id, access_key_id, secret_access_key, image_format, public_url):
        endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"

        s3_client = boto3.client(
            service_name='s3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name='auto'
        )
        pil_image = tensor_to_pil_image(image)
        # 2. 将 PIL Image 对象转换为字节流
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format=image_format)
        img_byte_arr.seek(0) # 将流的指针移到开头，以便从头开始读取

        # 3. 根据图像格式确定 Content-Type (MIME 类型)
        content_type_map = {
            "JPEG": "image/jpeg",
            "JPG": "image/jpeg",
            "PNG": "image/png",
            "WEBP": "image/webp",
        }
        content_type = content_type_map.get(image_format.upper(), "application/octet-stream")
        if content_type == "application/octet-stream":
            print(f"警告: 未知图像格式 '{image_format}'，使用默认 Content-Type: application/octet-stream。")

        s3_client.put_object(
            Bucket=bucket,
            Key=key_name,
            Body=img_byte_arr,
            ContentType=content_type
        )

        if public_url:
            if not public_url.startswith("https://"):
                public_url = f"https://{public_url}"
            full_url = f"{public_url}/{key_name}"
        else:
            full_url = f"https://{account_id}.r2.cloudflarestorage.com/{bucket}/{key_name}"

        return (full_url, )
