import time
import torch
import httpx
from io import BytesIO
from PIL import Image as PILImage
from huggingface_hub import InferenceClient, ImageToImageTargetSize
from .utils import tensor_to_pil_image, convert_pil_image_to_base64, convert_base64_to_image, pil_image_to_tensor


class OpenRouterImage:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "openrouter_api_key": ("STRING", {"multiline": False}),
                "model": (
                    [
                        "bytedance-seed/seedream-4.5",
                        "google/gemini-3-pro-image-preview",
                        "black-forest-labs/flux.2-max",
                        "sourceful/riverflow-v2-max-preview",
                        "sourceful/riverflow-v2-standard-preview",
                        "black-forest-labs/flux.2-pro",
                        "google/gemini-2.5-flash-image",
                        "openai/gpt-5-image-mini",
                        "openai/gpt-5-image",
                    ],
                    {"default": "bytedance-seed/seedream-4.5"}
                ),
                "aspect_ratio": ([
                    "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9",
                ], {"default": "3:4"})
            },
            "optional": {
                "image": ("IMAGE", {"default": None}),
                "base_url": ("STRING", {"multiline": False, "default": "https://openrouter.ai/api"}),
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
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "assistant")
    FUNCTION = "gen_openrouter_gemini_flash_image"

    CATEGORY = "AIToolkits/Image2Image"

    @staticmethod
    def gen_openrouter_gemini_flash_image(prompt: str, openrouter_api_key, model:str, aspect_ratio: str="3:4", image=None, base_url="https://openrouter.ai/api", seed=0):
        user_content_parts = [{
            "type": "text",
            "text": prompt
        }]

        if image is not None:
            # image 是一个 (B, H, W, C) 的张量
            for i in range(image.shape[0]):
                # 提取批次中的单张图片 (1, H, W, C)
                current_input_image_tensor = image[i].unsqueeze(0)
                pil_img = tensor_to_pil_image(current_input_image_tensor)
                base64_img = convert_pil_image_to_base64(pil_img)
                user_content_parts.append({
                    "type": "image_url",
                    "image_url": {
                        "url": base64_img,
                    }
                })

        messages = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt if image is None else user_content_parts
                }
            ],
            "modalities": ["image", "text"],
            "image_config": {
                "aspect_ratio": aspect_ratio,
            }
        }

        with httpx.Client() as http_client:
            response = http_client.post(
                url=f"{base_url}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_api_key}",
                    "Content-Type": "application/json",
                },
                json=messages,
                timeout=600,
            )
            response.raise_for_status()
            result = response.json()

        all_images = []
        if 'choices' in result and len(result['choices']) > 0 and 'message' in result['choices'][0] and 'images' in result['choices'][0]['message']:
            for img in result['choices'][0]['message']['images']:
                img_url = img['image_url']['url']
                pil_img = convert_base64_to_image(img_url)
                output_tensor = pil_image_to_tensor(pil_img)
                all_images.append(output_tensor)
            content = result['choices'][0]['message']['content']
            batch_tensor = torch.cat(all_images, dim=0)
            return batch_tensor, content
        else:
            raise Exception(f"OpenRouter API 响应中未找到图片。响应内容: {result}")


class ModelScopeQwenImageEdit:
    url: str = "https://api-inference.modelscope.cn/v1/images/generations"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
                "prompt": ("STRING", {"multiline": True}),
                "model": (
                    [
                        "Qwen/Qwen-Image-Edit",
                        "Qwen/Qwen-Image-Edit-2511",
                    ], {"default": "Qwen/Qwen-Image-Edit"}),
                "image_url": ("STRING", {"multiline": False}),
                "width": ("INT", {"default": 1024}),
                "height": ("INT", {"default": 1024}),
                "steps": ("INT", {"default": 25, "min": 1, "max": 100, "step": 1}),
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
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "modelscope_qwen_image_edit"

    CATEGORY = "AIToolkits/Image2Image"

    def modelscope_qwen_image_edit(self, api_key: str, prompt: str, model: str, image_url: str, width: int, height: int, steps: int, seed=0):
        common_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client() as http_client:
            params: dict = {
                "model": model,
                "prompt": prompt,
                "image_url": image_url,
                "size": f"{width}x{height}",
                "steps": steps,
            }
            response = http_client.post(
                self.url,
                headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
                json=params,
            )

            response.raise_for_status()
            task_id = response.json()["task_id"]

            while True:
                result = http_client.get(
                    f"https://api-inference.modelscope.cn/v1/tasks/{task_id}",
                    headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
                )
                result.raise_for_status()
                data = result.json()

                if data["task_status"] == "SUCCEED":
                    pil_image = PILImage.open(
                        BytesIO(httpx.get(data["output_images"][0]).content)
                    )
                    break
                elif data["task_status"] == "FAILED":
                    raise Exception(data)

                time.sleep(5)

        output_tensor = pil_image_to_tensor(pil_image)
        return (output_tensor,)


class SeedreamImage:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "api_key": ("STRING", {"multiline": False}),
                "model": (
                    [
                        "doubao-seedream-4-5-251128",
                        "doubao-seedream-4-0-250828",
                    ],
                    {"default": "doubao-seedream-4-5-251128"}
                ),
                "size": (
                    [
                        "1728x2304",
                        "2048x2048",
                        "2304x1728",
                        "2560x1440",
                        "1440x2560",
                        "2496x1664",
                        "1664x2496",
                        "3024x1296",
                    ],
                    {"default": "1728x2304"}
                ),
                "max_images": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1}),
            },
            "optional": {
                "image": ("IMAGE", {"default": None}),
                "base_url": ("STRING", {"multiline": False, "default": "https://ark.cn-beijing.volces.com/api"}),
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
            }
        }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    FUNCTION = "gen_seedream_image"

    CATEGORY = "AIToolkits/Image2Image"

    @staticmethod
    def gen_seedream_image(prompt: str, api_key, model:str, image=None, size="1728x2304", max_images=1, base_url="https://ark.cn-beijing.volces.com/api", seed=0):

        url = f'{base_url}/v3/images/generations'

        user_images = []

        if image is not None:
            for i in range(image.shape[0]):
                current_input_image_tensor = image[i].unsqueeze(0)
                pil_img = tensor_to_pil_image(current_input_image_tensor)
                base64_img = convert_pil_image_to_base64(pil_img)
                user_images.append(base64_img)


        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload: dict = {
            "model": model,
            "prompt": prompt,
            "sequential_image_generation": "auto",
            "sequential_image_generation_options": {
                "max_images": max_images
            },
            "response_format": "b64_json",
            "size": size,
            "stream": False,
            "watermark": False,
        }
        if user_images:
            payload['image'] = user_images


        try:
            with httpx.Client() as http_client:
                response = http_client.post(
                    url=url,
                    headers=headers,
                    json=payload,
                    timeout=600,
                )
                response.raise_for_status()
                result = response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"API 响应错误: {e.response.json()}")

        all_images = []
        if 'data' in result:
            for img in result['data']:
                img_base64 = img['b64_json']
                pil_img = convert_base64_to_image(img_base64)
                output_tensor = pil_image_to_tensor(pil_img)
                all_images.append(output_tensor)
            batch_tensor = torch.cat(all_images, dim=0)
            return (batch_tensor,)
        else:
            raise Exception(f"API 响应中未找到图片。响应内容: {result}")


class HFImageToImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
                "image": ("IMAGE", {"default": None}),
                "prompt": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "width": ("INT", {"default": 1024}),
                "height": ("INT", {"default": 1024}),
                "steps": ("INT", {"default": 25, "min": 1, "max": 100, "step": 1}),
                "guidance_scale": ("FLOAT", {"default": 3.5}),
                "model": (
                    [
                        "Qwen/Qwen-Image-Edit-2509",
                        "black-forest-labs/FLUX.2-dev",
                        "meituan-longcat/LongCat-Image-Edit",
                        "dx8152/Qwen-Edit-2509-Multiple-angles",
                        "black-forest-labs/FLUX.1-Kontext-dev",
                        "starsfriday/Qwen-Image-Edit-2509-Upscale2K",
                        "dx8152/Qwen-Image-Edit-2509-Light_restoration",
                    ],
                    {"default": "Qwen/Qwen-Image-Edit-2509"},
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
    FUNCTION = "hf_image_to_image"
    CATEGORY = "AIToolkits/HuggingFace"

    @staticmethod
    def hf_image_to_image(
            api_key: str,
            image,
            prompt: str,
            width: int,
            height: int,
            steps,
            guidance_scale: float,
            model="Qwen/Qwen-Image-Edit-2509",
            seed: int = 0,
    ):
        client = InferenceClient(
            provider="auto",
            api_key=api_key,
        )

        output_images = []

        for i in range(image.shape[0]):
            current_input_image_tensor = image[i].unsqueeze(0)
            pil_img = tensor_to_pil_image(current_input_image_tensor)

            result_pil = client.image_to_image(
                pil_img,
                prompt,
                model=model,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                target_size=ImageToImageTargetSize(height=height, width=width),
                seed=seed,
            )
            output_images.append(pil_image_to_tensor(result_pil))

        return (torch.cat(output_images, dim=0),)
