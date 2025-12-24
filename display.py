class HtmlIFramePreviewer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "html_or_url": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "html_iframe_preview"
    CATEGORY = "AIToolkits/Display"

    @staticmethod
    def html_iframe_preview(html_or_url: str):
        return {"ui": {"html": [html_or_url]}}


class HTMLPreviewer:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "html_string": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "html_preview"
    CATEGORY = "AIToolkits/Display"

    @staticmethod
    def html_preview(html_string):
        # 为了让 ComfyUI 知道这个节点执行了并产生了结果，
        # 我们需要在返回的 tuple 中包含一个 UI 部分。
        # 这里我们返回原始的 html_string，让前端去处理。
        return {"ui": {"html": [html_string]}, "result": (html_string,)}


class CodeViewer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "code": ("STRING", {"multiline": False, "default": "", "forceInput": True}),
            },
            "optional": {
                "code_format": (["python", "javascript", "typescript", "ts-jsx", "vue", "html", "json", "angular"], {"default": "python"}),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "view_code"
    CATEGORY = "AIToolkits/Display"

    @staticmethod
    def view_code(code: str, code_format: str = "python"):
        return {"ui": {"code": [code], "code_format": [code_format]}}


class MarkDownViewer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "markdown": ("STRING", {"multiline": False, "default": "", "forceInput": True}),
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "view_markdown"
    CATEGORY = "AIToolkits/Display"

    @staticmethod
    def view_markdown(markdown: str):
        return {"ui": {"markdown": [markdown]}}
