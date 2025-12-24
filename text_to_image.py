import time
import httpx
import folder_paths
from io import BytesIO
from PIL import Image as PILImage
from huggingface_hub import InferenceClient
from .utils import pil_image_to_tensor


MAX_DIMENSION = 980
DASHSCOPE_API_URL = (
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
)


class ModelScopeTextToImage:
    url: str = "https://api-inference.modelscope.cn/v1/images/generations"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False, "dynamicPrompts": False}),
                "prompt": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "width": ("INT", {"default": 1024}),
                "height": ("INT", {"default": 1024}),
                "steps": ("INT", {"default": 25, "min": 1, "max": 100, "step": 1}),
                "model": (
                    [
                        "Tongyi-MAI/Z-Image-Turbo",
                        "black-forest-labs/FLUX.2-dev",
                        "black-forest-labs/FLUX.1-Krea-dev",
                        "Qwen/Qwen-Image",
                        "KookYan/Kook_xieshi_Kook_Qwen_V2",
                        "MAILAND/majicflus_v1",
                        "MusePublic/489_ckpt_FLUX_1",
                        "yiwanji/FLUX_xiao_hong_shu_ji_zhi_zhen_shi_V2",
                        "movietalk/jimeng",
                        "sd1995/lora_rioko_kontext",
                        "MusePublic/majicMIX_realistic",
                        "MusePublic/FluxUltraRealistic",
                        "sd1995/lora_ikoras_kontext",
                        "DonRat/MAJICFLUS_Superplastic",
                    ],
                    {"default": "Tongyi-MAI/Z-Image-Turbo"},
                ),
            },
            "optional": {
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "step": 1,
                        "display": "number",
                    },
                ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "modelscope_text_to_image"
    CATEGORY = "AIToolkits/Text2Image"

    def modelscope_text_to_image(
        self,
        api_key: str,
        prompt: str,
        width: int,
        height: int,
        steps: int = 25,
        model="black-forest-labs/FLUX.1-Krea-dev",
        seed: int = 0,
    ):
        payload = {
            "model": model,
            "prompt": prompt,
            "size": f"{width}x{height}",
            "steps": steps,
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        res = httpx.post(
            self.url,
            json=payload,
            headers={
                **headers,
                "X-ModelScope-Async-Mode": "true",
            },
            timeout=360,
        )
        if res.status_code != 200:
            raise Exception(res.content)
        result = res.json()
        task_id = result["task_id"]

        while True:
            task_status = httpx.get(
                f"https://api-inference.modelscope.cn/v1/tasks/{task_id}",
                headers={**headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            task_status.raise_for_status()
            task_data = task_status.json()
            if task_data["task_status"] == "SUCCEED":
                pil_image = PILImage.open(
                    BytesIO(httpx.get(task_data["output_images"][0]).content)
                )
                break
            elif task_data["task_status"] == "FAILED":
                raise Exception(task_data)

            time.sleep(4)

        output_tensor = pil_image_to_tensor(pil_image)
        return (output_tensor,)


class HFTextToImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
                "prompt": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "width": ("INT", {"default": 1024}),
                "height": ("INT", {"default": 1024}),
                "steps": ("INT", {"default": 25, "min": 1, "max": 100, "step": 1}),
                "guidance_scale": ("FLOAT", {"default": 3.5}),
                "model": (
                    [
                        "Tongyi-MAI/Z-Image-Turbo",
                        "Shakker-Labs/AWPortrait-Z",
                        "Qwen/Qwen-Image",
                        "meituan-longcat/LongCat-Image",
                        "black-forest-labs/FLUX.1-Krea-dev"
                    ],
                    {"default": "Tongyi-MAI/Z-Image-Turbo"},
                ),
            },
            "optional": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xFFFFFFFFFFFFFFFF,
                    "step": 1,
                    "display": "number",
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "hf_text_to_image"
    CATEGORY = "AIToolkits/Text2Image"

    @staticmethod
    def hf_text_to_image(
        api_key: str,
        prompt: str,
        width: int,
        height: int,
        steps,
        guidance_scale: float,
        model="Tongyi-MAI/Z-Image-Turbo",
        seed: int = 0,
    ):
        client = InferenceClient(
            provider="auto",
            api_key=api_key,
        )

        result_image = client.text_to_image(
            prompt,
            model=model,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            seed=seed,
        )
        output_tensor = pil_image_to_tensor(result_image)
        return (output_tensor,)
