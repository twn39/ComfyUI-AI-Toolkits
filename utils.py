import io
import torch
import base64
import numpy as np
from PIL import Image
from torchvision.transforms.functional import to_pil_image


def pil_image_to_tensor(image: Image.Image):
    pil_image = image.convert("RGB")
    np_image = np.array(pil_image)
    if np_image.dtype == np.uint8:
        np_image = np_image.astype(np.float32) / 255.0
    elif np_image.dtype != np.float32:
        np_image = np_image.astype(np.float32)
    output_tensor = torch.from_numpy(np_image).unsqueeze(0)
    output_tensor = output_tensor.cpu()
    return output_tensor


def tensor_to_pil_image(image) -> Image.Image:
    tensor_image = image.squeeze(0).permute(2, 0, 1)
    pil_img = to_pil_image(tensor_image)
    return pil_img


def convert_base64_to_image(b64_string: str) -> Image.Image:
    if not isinstance(b64_string, str) or not b64_string:
        raise ValueError("输入不是一个有效的字符串。")

    if ',' in b64_string:
        base64_data = b64_string.split(',')[1]
    else:
        base64_data = b64_string
    try:
        image_bytes = base64.b64decode(base64_data)
        image_buffer = io.BytesIO(image_bytes)
        img = Image.open(image_buffer)
        return img
    except Exception as e:
        print("PIL 无法识别图像文件。这通常意味着 Base64 字符串代表的不是图像数据。")
        raise e

def convert_pil_image_to_base64(img: Image.Image) -> str:
    buffered = io.BytesIO()
    img_format = "PNG" if img.mode in ("RGBA", "LA") else "JPEG"
    img.save(buffered, format=img_format)
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/{'png' if img_format == 'PNG' else 'jpeg'};base64,{base64_image}"
