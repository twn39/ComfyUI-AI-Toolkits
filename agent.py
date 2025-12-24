import io
from typing import List
from PIL.Image import Resampling
from openai import OpenAI
from agno.media import Image
from dataclasses import dataclass
from agno.agent import Agent
from agno.models.base import Model
from agno.models.openai import OpenAILike
from agno.models.deepseek import DeepSeek
from agno.tools.jina import JinaReaderTools

from .utils import tensor_to_pil_image
from .agent_tools import math_expr

MAX_DIMENSION = 980


@dataclass
class Vision:
    openai: OpenAI
    model: str
    temperature: float
    max_tokens: int


class OpenAILikeModel:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("STRING", {"multiline": False, "dynamicPrompts": False}),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0, "max": 2}),
                "max_tokens": ("INT", {"default": 4096, "min": 250, "max": 40960}),
                "api_key": ("STRING", {"multiline": False, "dynamicPrompts": False}),
                "base_url": ("STRING", {"multiline": False, "dynamicPrompts": False}),
            },
        }

    RETURN_TYPES = ("LLMModel",)
    FUNCTION = "gen_llm_model"

    CATEGORY = "AIToolkits/Agents/LLMProviders"

    @staticmethod
    def gen_llm_model(
        model="", temperature=0.3, max_tokens=4096, api_key=None, base_url=None
    ):
        llm_client = OpenAILike(
            id=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return (llm_client,)


class DeepSeekModel:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (["deepseek-chat", "deepseek-reasoner"],),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0, "max": 2}),
                "max_tokens": ("INT", {"default": 4096, "min": 250, "max": 40960}),
                "api_key": ("STRING", {"multiline": False, "dynamicPrompts": False}),
            },
        }

    RETURN_TYPES = ("LLMModel",)
    FUNCTION = "gen_deepseek_model"

    CATEGORY = "AIToolkits/Agents/LLMProviders"

    @staticmethod
    def gen_deepseek_model(
        model="deepseek-chat", temperature=0.3, max_tokens=4096, api_key=None
    ):
        llm_client = DeepSeek(
            id=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url="https://api.deepseek.com/v1",
        )
        return (llm_client,)



class QwenModel:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (
                    [
                        "qwen2.5-72b-instruct",
                        "qwen2.5-32b-instruct",
                        "qwen2.5-vl-72b-instruct",
                        "qwen2.5-vl-32b-instruct",
                    ],
                ),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0, "max": 2}),
                "max_tokens": ("INT", {"default": 4096, "min": 250, "max": 40960}),
                "api_key": ("STRING", {"multiline": False, "dynamicPrompts": False}),
            },
        }

    RETURN_TYPES = ("LLMModel",)
    FUNCTION = "gen_qwen_model"

    CATEGORY = "AIToolkits/Agents/LLMProviders"

    @staticmethod
    def gen_qwen_model(
        model="qwen2.5-32b-instruct", temperature=0.3, max_tokens=4096, api_key=None
    ):
        llm_client = OpenAILike(
            id=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        return (llm_client,)


class ModelScopeModel:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (
                    [
                        "ZhipuAI/GLM-4.7",
                        "Qwen/Qwen3-Coder-480B-A35B-Instruct",
                        "Qwen/Qwen3-235B-A22B-Thinking-2507",
                        "Qwen/Qwen3-235B-A22B-Instruct-2507",
                        "ZhipuAI/GLM-4.5",
                        "stepfun-ai/step3",
                        "Qwen/Qwen3-32B",
                        "deepseek-ai/DeepSeek-R1-0528",
                        "Qwen/Qwen2.5-VL-72B-Instruct",
                        "Qwen/Qwen2.5-VL-32B-Instruct",
                    ],
                    {"default": "ZhipuAI/GLM-4.7"},
                ),
                "temperature": (
                    "FLOAT",
                    {"default": 0.3, "min": 0, "max": 2, "step": 0.1},
                ),
                "max_tokens": (
                    "INT",
                    {"default": 4096, "min": 250, "max": 40960, "step": 1024},
                ),
                "api_key": ("STRING", {"multiline": False, "dynamicPrompts": False}),
            },
        }

    RETURN_TYPES = ("LLMModel",)
    FUNCTION = "gen_modelscope_model"

    CATEGORY = "AIToolkits/Agents/LLMProviders"

    @staticmethod
    def gen_modelscope_model(
        model: str, temperature=0.3, max_tokens=4096, api_key=None
    ):
        llm_client = OpenAILike(
            id=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            base_url="https://api-inference.modelscope.cn/v1",
        )
        return (llm_client,)


class OpenRouterModel:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": (
                    [
                        "z-ai/glm-4.7",
                        "minimax/minimax-m2.1",
                        "google/gemini-3-flash-preview",
                        "openai/gpt-5.2",
                        "deepseek/deepseek-v3.2",
                        "x-ai/grok-4.1-fast",
                        "google/gemini-3-pro-preview",
                        "moonshotai/kimi-k2-thinking",
                        "z-ai/glm-4.6v",
                        "openai/gpt-5.1",
                        "anthropic/claude-opus-4.5",
                        "google/gemini-2.5-flash-preview-09-2025",
                        "anthropic/claude-sonnet-4.5",
                        "qwen/qwen3-vl-235b-a22b-instruct",
                        "qwen/qwen3-vl-235b-a22b-thinking",
                        "z-ai/glm-4.6",
                        "openai/gpt-5-codex",
                        "x-ai/grok-4-fast",
                        "qwen/qwen3-vl-30b-a3b-instruct",
                        "qwen/qwen3-vl-30b-a3b-thinking",
                        "qwen/qwen3-max",
                        "moonshotai/kimi-k2-0905",
                        "x-ai/grok-code-fast-1",
                        "qwen/qwen3-235b-a22b-07-25",
                        "google/gemini-2.5-flash",
                        "google/gemini-2.5-pro",
                        "qwen/qwen3-32b",
                        "openai/gpt-4.1",
                        "openai/gpt-5",
                        "openai/gpt-5-mini",
                        "openai/gpt-oss-120b",
                        "z-ai/glm-4.5v",
                        "openai/o4-mini-high",
                        "anthropic/claude-3.7-sonnet",
                        "anthropic/claude-3.7-sonnet:thinking",
                    ],
                ),
                "temperature": ("FLOAT", {"default": 0.3, "min": 0, "max": 2}),
                "max_tokens": ("INT", {"default": 4096, "min": 250, "max": 40960}),
                "api_key": ("STRING", {"multiline": False, "dynamicPrompts": False}),
            },
        }

    RETURN_TYPES = ("LLMModel",)
    FUNCTION = "gen_openrouter_model"

    CATEGORY = "AIToolkits/Agents/LLMProviders"

    @staticmethod
    def gen_openrouter_model(
        model="qwen/qwen3-235b-a22b-07-25",
        temperature=0.3,
        max_tokens=4096,
        api_key=None,
    ):
        llm_client = OpenAILike(
            id=model,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return (llm_client,)


class SimpleAgent:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "llm_model": ("LLMModel",),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "debug_mode": ([True, False], {"default": False}),
            },
            "optional": {
                "image": ("IMAGE",),
                "tools": ("AGENT_TOOLS", {"default": None}),
                "system_prompt": (
                    "STRING",
                    {"default": None, "multiline": True, "forceInput": True},
                ),
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

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "text_agent_run"

    CATEGORY = "AIToolkits/Agents"

    @staticmethod
    def text_agent_run(llm_model: Model, prompt: str, debug_mode: bool, image=None, tools=None, system_prompt: str=None, seed: int=0):
        media_images: List[Image] = []
        if image is not None:
            pil_image = tensor_to_pil_image(image)
            pil_image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Resampling.LANCZOS)
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format="JPEG")
            img_content = img_byte_arr.getvalue()
            media_images.append(Image(content=img_content))
        if tools is not None:
            if not isinstance(tools, list):
                tools = [tools]
        agent = Agent(
            model=llm_model,
            debug_mode=debug_mode,
            system_message=system_prompt,
            retries=3,
            tools=tools,
        )
        response = agent.run(prompt, images=media_images)
        return (response.content,)



class ChatAgent:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "llm_model": ("LLMModel",),
                "show_tool_calls": ([True, False], {"default": False}),
                "debug_mode": ([True, False], {"default": False}),
            },
            "optional": {
                "tools": ("AGENT_TOOLS", {"default": None}),
                "system_prompt": (
                    "STRING",
                    {"default": None, "multiline": True, "forceInput": True},
                ),
            },
        }

    RETURN_TYPES = ("AGENT",)
    RETURN_NAMES = ("agent",)
    FUNCTION = "chat_agent_run"
    CATEGORY = "AIToolkits/Agents"

    @staticmethod
    def chat_agent_run(llm_model: Model, show_tool_calls: bool, debug_mode: bool, tools=None, system_prompt: str=None):
        if tools is not None:
            if not isinstance(tools, list):
                tools = [tools]

        agent = Agent(
            model=llm_model,
            debug_mode=debug_mode,
            tools=tools,
            enable_agentic_memory=False,
            enable_user_memories=False,
            system_message=system_prompt,
            retries=3,
        )
        return (agent, )


class AgentChain:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "agent": ("AGENT",),
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "llm_model": ("LLMModel",),
                "image": ("IMAGE",),
                "tools": ("AGENT_TOOLS", {"default": None}),
            },
        }

    RETURN_TYPES = ("AGENT", "STRING", "STRING")
    RETURN_NAMES = ("agent", "assistant", "history messages")
    FUNCTION = "agent_chain_run"
    CATEGORY = "AIToolkits/Agents"

    @staticmethod
    def agent_chain_run(agent: Agent, prompt: str, llm_model=None, image=None, tools=None):
        media_images: List[Image] = []
        if image is not None:
            pil_image = tensor_to_pil_image(image)
            pil_image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Resampling.LANCZOS)
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format="JPEG")
            img_content = img_byte_arr.getvalue()
            media_images.append(Image(content=img_content))
        if llm_model is not None:
            agent.model = llm_model
        if tools is not None:
            if not isinstance(tools, list):
                tools = [tools]
            agent.tools = tools
        res = agent.run(prompt, images=media_images)
        history_messages = [m.model_dump(include={"role", "content", "images"}) for m in agent.get_messages_for_session()]
        return agent, res.content, history_messages


class AgentMathTools:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {},
        }

    RETURN_TYPES = ("AGENT_TOOLS",)
    RETURN_NAMES = ("tool", )
    FUNCTION = "get_math_tools"

    CATEGORY = "AIToolkits/Agents/Tools"

    @staticmethod
    def get_math_tools():
        return (math_expr,)


class AgentJinaReaderTools:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"multiline": False, "dynamicPrompts": False}),
                "max_content_length": ("INT", {"default": 10000, "min": 1000, "max": 1000000, "step": 1000}),
                "timeout": ("INT", {"default": 60, "min": 10, "max": 300, "step": 10}),
            },
        }

    RETURN_TYPES = ("AGENT_TOOLS",)
    RETURN_NAMES = ("tool", )
    FUNCTION = "get_jina_reader_tools"

    CATEGORY = "AIToolkits/Agents/Tools"

    @staticmethod
    def get_jina_reader_tools(api_key: str, max_content_length: int=10000, timeout: int=60):
        tool = JinaReaderTools(api_key, max_content_length=max_content_length, timeout=timeout)
        return (tool,)


class AgentMergeTools:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "tool": ("AGENT_TOOLS",),
                "tool1": ("AGENT_TOOLS",),
            },
            "optional": {
                "tool2": ("AGENT_TOOLS",),
                "tool3": ("AGENT_TOOLS",),
            },
        }

    RETURN_TYPES = ("AGENT_TOOLS",)
    RETURN_NAMES = ("tools", )
    FUNCTION = "merge_tools"

    CATEGORY = "AIToolkits/Agents/Tools"

    @staticmethod
    def merge_tools(tool, tool1, tool2=None, tool3=None):
        tools = []
        if isinstance(tool, list):
            tools = tools + tool
        else:
            tools.append(tool)
        if isinstance(tool1, list):
            tools = tools + tool1
        else:
            tools.append(tool1)
        if tool2 is not None:
            if isinstance(tool2, list):
                tools = tools + tool2
            else:
                tools.append(tool2)
        if tool3 is not None:
            if isinstance(tool3, list):
                tools = tools + tool3
            else:
                tools.append(tool3)
        return (tools, )
