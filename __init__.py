from .image_to_image import (
    OpenRouterImage,
    ModelScopeQwenImageEdit,
    SeedreamImage,
    HFImageToImage,
)
from .cloud_storage import (
    CloudflareR2
)
from .common import (
    JSONParse,
    MDConvert,
    PromptMerge,
    EmptyChatMessages,
)

from .text_to_image import (
    ModelScopeTextToImage,
    HFTextToImage,
)

from .openai_native import (
    OpenAiNative,
    OpenAiNativeChat,
    OpenAiModelScope,
    OpenAiOpenRouter,
    OpenAiJinaAI,
    OpenAiHuggingFace,
    OpenAiDashScope,
    OpenAiDeepSeek,
)

from .agent import (
    OpenAILikeModel,
    DeepSeekModel,
    QwenModel,
    OpenRouterModel,
    SimpleAgent,
    ModelScopeModel,
    AgentChain,
    ChatAgent,
    AgentMathTools,
    AgentMergeTools,
    AgentJinaReaderTools,
)

from .data import (
    DataFrameLoader,
    DatePicker,
    TextFileLoader,
    TextSaver,
)

from .finance import (
    AKShareStockHistory,
    AKShareMacroChinaCPI,
    AKShareMacroChinaPPI,
    YfinanceTicker,
)

from .visualization import (
    MatplotlibVisualization,
    PlotlyVisualization,
    BokehVisualization,
    MermaidChart,
)

from .display import (
    HTMLPreviewer,
    HtmlIFramePreviewer,
    CodeViewer,
    MarkDownViewer,
)

NODE_CLASS_MAPPINGS = {
    "OpenAILikeModel": OpenAILikeModel,
    "DeepSeekModel": DeepSeekModel,
    "QwenModel": QwenModel,
    "ModelScopeModel": ModelScopeModel,
    "OpenRouterModel": OpenRouterModel,
    "SimpleAgent": SimpleAgent,
    "DataFrameLoader": DataFrameLoader,
    "OpenAiNative": OpenAiNative,
    "EmptyChatMessages": EmptyChatMessages,
    "OpenAiNativeChat": OpenAiNativeChat,
    "AgentMathTools": AgentMathTools,
    "JSONParse": JSONParse,
    "ModelScopeTextToImage": ModelScopeTextToImage,
    "HFTextToImage": HFTextToImage,
    "MDConvert": MDConvert,
    "HTMLPreviewer": HTMLPreviewer,
    "TextFileLoader": TextFileLoader,
    "AgentMergeTools": AgentMergeTools,
    "AgentJinaReaderTools": AgentJinaReaderTools,
    "TextSaver": TextSaver,
    "MatplotlibVisualization": MatplotlibVisualization,
    "AKShareStockHistory": AKShareStockHistory,
    "HtmlIFramePreviewer": HtmlIFramePreviewer,
    "PlotlyVisualization": PlotlyVisualization,
    "BokehVisualization": BokehVisualization,
    "MermaidChart": MermaidChart,
    "CodeViewer": CodeViewer,
    "AKShareMacroChinaCPI": AKShareMacroChinaCPI,
    "AKShareMacroChinaPPI": AKShareMacroChinaPPI,
    "DatePicker": DatePicker,
    "YfinanceTicker": YfinanceTicker,
    "OpenAiModelScope": OpenAiModelScope,
    "OpenAiOpenRouter": OpenAiOpenRouter,
    "OpenAiJinaAI": OpenAiJinaAI,
    "OpenAiHuggingFace": OpenAiHuggingFace,
    "OpenAiDashScope": OpenAiDashScope,
    "OpenAiDeepSeek": OpenAiDeepSeek,
    "PromptMerge": PromptMerge,
    "MarkDownViewer": MarkDownViewer,
    "AgentChain": AgentChain,
    "ChatAgent": ChatAgent,
    "CloudflareR2": CloudflareR2,
    "OpenRouterImage": OpenRouterImage,
    "ModelScopeQwenImageEdit": ModelScopeQwenImageEdit,
    "SeedreamImage": SeedreamImage,
    "HFImageToImage": HFImageToImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DataFrameLoader": "Pandas dataframe 加载器",
    "OpenAiNative": "OpenAI 原生接口",
    "EmptyChatMessages": "空对话消息",
    "OpenAiNativeChat": "OpenAI 原生接口-对话",
    "AgentChat": "对话代理",
    "AgentMathTools": "数学工具",
    "JSONParse": "JSON 解析器",
    "ModelScopeTextToImage": "ModelScope 文生图",
    "HFTextToImage": "HuggingFace 文生图",
    "MDConvert": "Markdown 转换",
    "HTMLPreviewer": "HTML 预览器",
    "SimpleAgent": "Simple Agent",
    "TextFileLoader": "文本文件加载器",
    "AgentMergeTools": "工具合并",
    "ModelScopeModel": "ModelScope 模型",
    "AgentJinaReaderTools": "Jina 阅读工具",
    "TextSaver": "文本保存器",
    "MatplotlibVisualization": "Matplotlib 可视化",
    "AKShareStockHistory": "AKShare 股票历史数据",
    "HtmlIFramePreviewer": "HTML IFrame 预览器",
    "PlotlyVisualization": "Plotly 可视化",
    "BokehVisualization": "Bokeh 可视化",
    "MermaidChart": "Mermaid 图表",
    "CodeViewer": "代码查看器",
    "AKShareMacroChinaCPI": "AKShare China CPI",
    "AKShareMacroChinaPPI": "AKShare China PPI",
    "DatePicker": "日期选择器",
    "YfinanceTicker": "Yahoo finance",
    "OpenAiModelScope": "OpenAI ModelScope",
    "OpenAiOpenRouter": "OpenAI OpenRouter",
    "OpenAiJinaAI": "OpenAI JinaAI",
    "OpenAiHuggingFace": "OpenAI HuggingFace",
    "OpenAiDashScope": "OpenAI DashScope",
    "OpenAiDeepSeek": "OpenAI DeepSeek",
    "PromptMerge": "Prompt 合并",
    "MarkDownViewer": "Markdown 预览器",
    "AgentChain": "Agent Chain",
    "ChatAgent": "Chat Agent",
    "CloudflareR2": "Cloudflare R2",
    "OpenRouterImage": "OpenRouter Image",
    "ModelScopeQwenImageEdit": "ModelScope Qwen Image Edit",
    "SeedreamImage": "Seedream Image Edit",
    "HFImageToImage": "HuggingFace Image Edit",
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
