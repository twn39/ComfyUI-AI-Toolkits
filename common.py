import json
from string import Template
import markdown2
from typing import Optional


class JSONParse:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": ("STRING", {"multiline": True,}),
            }
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("json", )
    FUNCTION = "json_parse"

    CATEGORY = "AIToolkits/Common"

    @staticmethod
    def json_parse(json_string: str):
        data = json.loads(json_string)
        return (data,)


class EmptyChatMessages:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "system_prompt": ("STRING", {"multiline": True, "default": "You are a helpful assistant."}),
                "user": ("STRING", {"multiline": False}),
            }
        }

    RETURN_TYPES = ("CHAT_MESSAGES",)
    RETURN_NAMES = ("chat_messages", )
    FUNCTION = "empty_chat_messages"

    CATEGORY = "AIToolkits/Common"

    @staticmethod
    def empty_chat_messages(system_prompt: str="You are a helpful assistant.", user: Optional[str]=None):
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        if user is not None and user != "":
            messages.append({"role": "user", "content": user})
        return (messages,)


class PromptMerge:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": False, "forceInput": True}),
                "p1": ("STRING", {"multiline": False, "forceInput": True}),
                "template": ("STRING", {"multiline": True, "placeholder": "$prompt"}),
            },
            "optional": {
                "p2": ("STRING", {"multiline": False, "forceInput": True}),
                "p3": ("STRING", {"multiline": False, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt", )
    FUNCTION = "prompt_merge"

    CATEGORY = "AIToolkits/Common"

    @staticmethod
    def prompt_merge(prompt: str, p1: str, template: str, p2: Optional[str]=None, p3: Optional[str]=None):
        t = Template(template)
        result = t.substitute(prompt=prompt, p1=p1, p2=p2, p3=p3)
        return (result,)


class MDConvert:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "markdown_text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("html_output",)
    FUNCTION = "md_convert"
    CATEGORY = "AIToolkits/Text/Markdown"

    def md_convert(self, markdown_text):
        html = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables", "spoiler"])
        return (html,)

