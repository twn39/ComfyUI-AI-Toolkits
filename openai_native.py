from openai import OpenAI
from typing import Optional

from .utils import tensor_to_pil_image, convert_pil_image_to_base64

MAX_DIMENSION = 980


class OpenAiNative:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
            },
            "optional": {
                "base_url": ("STRING", {"multiline": False, "default": None}),
            },
        }

    RETURN_TYPES = ("OPENAI_NATIVE_CLIENT",)
    RETURN_NAMES = ("openai_native_client",)
    FUNCTION = "openai_client"

    CATEGORY = "AIToolkits/OpenAI"

    @staticmethod
    def openai_client(api_key: str, base_url: str = None):
        if base_url is None:
            client = OpenAI(api_key=api_key)
        else:
            client = OpenAI(api_key=api_key, base_url=base_url)
        return (client,)


class OpenAiModelScope:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
            },
        }

    RETURN_TYPES = ("OPENAI_NATIVE_CLIENT",)
    RETURN_NAMES = ("openai_native_client",)
    FUNCTION = "openai_model_scope"

    CATEGORY = "AIToolkits/OpenAI/Providers"

    @staticmethod
    def openai_model_scope(api_key: str):
        client = OpenAI(
            api_key=api_key, base_url="https://api-inference.modelscope.cn/v1"
        )
        return (client,)


class OpenAiOpenRouter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
            },
        }

    RETURN_TYPES = ("OPENAI_NATIVE_CLIENT",)
    RETURN_NAMES = ("openai_native_client",)
    FUNCTION = "openai_openrouter"

    CATEGORY = "AIToolkits/OpenAI/Providers"

    @staticmethod
    def openai_openrouter(api_key: str):
        client = OpenAI(
            api_key=api_key, base_url="https://openrouter.ai/api/v1"
        )
        return (client,)


class OpenAiHuggingFace:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
            },
        }

    RETURN_TYPES = ("OPENAI_NATIVE_CLIENT",)
    RETURN_NAMES = ("openai_native_client",)
    FUNCTION = "openai_huggingface"

    CATEGORY = "AIToolkits/OpenAI/Providers"

    @staticmethod
    def openai_huggingface(api_key: str):
        client = OpenAI(
            api_key=api_key, base_url="https://router.huggingface.co/v1"
        )
        return (client,)


class OpenAiDeepSeek:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
            },
        }

    RETURN_TYPES = ("OPENAI_NATIVE_CLIENT",)
    RETURN_NAMES = ("openai_native_client",)
    FUNCTION = "openai_deepseek"

    CATEGORY = "AIToolkits/OpenAI/Providers"

    @staticmethod
    def openai_deepseek(api_key: str):
        client = OpenAI(
            api_key=api_key, base_url="https://api.deepseek.com/v1"
        )
        return (client,)


class OpenAiDashScope:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
            },
        }

    RETURN_TYPES = ("OPENAI_NATIVE_CLIENT",)
    RETURN_NAMES = ("openai_native_client",)
    FUNCTION = "openai_dashscope"

    CATEGORY = "AIToolkits/OpenAI/Providers"

    @staticmethod
    def openai_dashscope(api_key: str):
        client = OpenAI(
            api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        return (client,)


class OpenAiJinaAI:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False}),
            },
        }

    RETURN_TYPES = ("OPENAI_NATIVE_CLIENT",)
    RETURN_NAMES = ("openai_native_client",)
    FUNCTION = "openai_jina_ai"

    CATEGORY = "AIToolkits/OpenAI/Providers"

    @staticmethod
    def openai_jina_ai(api_key: str):
        client = OpenAI(
            api_key=api_key, base_url="https://deepsearch.jina.ai/v1"
        )
        return (client,)


class OpenAiNativeChat:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "client": ("OPENAI_NATIVE_CLIENT",),
                "prompt": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "model": ("STRING", {"multiline": False,},),
                "temperature": (
                    "FLOAT",
                    {"default": 0.3, "min": 0, "max": 2, "step": 0.1},
                ),
                "max_tokens": ("INT", {"default": 4096, "min": 250, "max": 40960}),
                "json_mode": ([False, True], {"default": False}),
            },
            "optional": {
                "messages": ("CHAT_MESSAGES", {"default": None}),
                "image": ("IMAGE", {"default": None}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xFFFFFFFFFFFFFFFF,
                    "step": 1,
                    "display": "number",
                }),
            },
        }

    RETURN_TYPES = ("CHAT_MESSAGES", "STRING")
    RETURN_NAMES = ("chat_messages", "assistant")
    FUNCTION = "openai_chat"

    CATEGORY = "AIToolkits/OpenAI"

    @staticmethod
    def openai_chat(
        client: OpenAI,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        json_mode: bool=False,
        messages: Optional[list]=None,
        image=None,
        seed: int = 0,
    ):
        if messages is None:
            messages = []
        if image is not None:
            pil_img = tensor_to_pil_image(image)
            pil_img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))
            base64_image_url = convert_pil_image_to_base64(pil_img)
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64_image_url,
                            },
                        },
                    ],
                }
            )
        else:
            messages.append({"role": "user", "content": prompt})

        response_format = {"type": "json_object"} if json_mode else {"type": "text"}
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
            extra_body={"enable_thinking": json_mode},
        )
        content = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": content})
        return messages, content
