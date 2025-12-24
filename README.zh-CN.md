<div align="center">

# ComfyUI AI 工具包

![GitHub Repo stars](https://img.shields.io/github/stars/twn39/ComfyUI-AI-Toolkits?style=flat-square) ![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg?style=flat-square) ![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg?style=flat-square) ![Version](https://img.shields.io/badge/version-0.1.0-orange.svg?style=flat-square) ![ComfyUI](https://img.shields.io/badge/ComfyUI-✓-green.svg?style=flat-square)

![Screenshot](screenshot/screenshot.png)

ComfyUI 的 AI 节点综合集合，可在工作流中无缝集成大语言模型、图像生成、数据分析、金融数据、可视化和云存储。

</div>

## 功能特性

- **AI 智能体**：支持多个 LLM 提供商（OpenAI 兼容、DeepSeek、Qwen、ModelScope、OpenRouter），具备工具调用能力。
- **文本生成图像**：使用 ModelScope 和 Hugging Face 推理提供商从提示词生成图像。
- **图像编辑**：使用 OpenRouter（Gemini/GPT-5-image）、ModelScope Qwen、Seedream 和 Hugging Face 模型编辑或转换图像。
- **数据处理**：加载 CSV 数据、选择日期、读/写文本文件。
- **金融数据**：通过 AKShare 获取股票历史、中国 CPI/PPI，以及 Yahoo Finance 数据。
- **可视化**：通过 AI 驱动的代码生成创建图表（Matplotlib、Plotly、Bokeh）和 Mermaid 图表。
- **显示与预览**：直接在 ComfyUI 中预览 HTML、代码和 Markdown。
- **云存储**：将图像上传到 Cloudflare R2 并生成公开 URL。
- **实用工具**：JSON 解析、Markdown 转 HTML 转换、提示词模板等。

## 安装

### 前置要求
- Python 3.11 或更高版本（推荐；参见 `.python-version`）
- 已安装并运行 ComfyUI

### 安装步骤

1. **克隆仓库**到 ComfyUI 的 `custom_nodes` 文件夹：
   ```bash
   cd /path/to/ComfyUI/custom_nodes
   git clone https://github.com/twn39/ComfyUI-AI-Toolkits.git
   ```

2. **安装 Python 依赖**（建议使用虚拟环境）：
   ```bash
   cd ComfyUI-AI-Toolkits
   pip install -r requirements.txt
   ```

3. **重启 ComfyUI**。节点将出现在 `AIToolkits` 类别下。


## 节点分类与列表

### AI 智能体 / LLM 提供商
| 节点 | 描述 |
|------|-------------|
| `OpenAILikeModel` | 通用 OpenAI 兼容模型客户端 |
| `DeepSeekModel` | DeepSeek 聊天/推理模型 |
| `QwenModel` | 通过 DashScope 的 Qwen 模型 |
| `ModelScopeModel` | ModelScope 托管模型 |
| `OpenRouterModel` | OpenRouter 模型（Gemini、GPT-5、Claude 等） |
| `SimpleAgent` | 使用提示词和可选图像/工具运行智能体 |
| `ChatAgent` | 创建具有记忆功能的对话智能体 |
| `AgentChain` | 链接多个智能体步骤 |
| `AgentMathTools` | 提供数学表达式求值工具 |
| `AgentJinaReaderTools` | 用于网页/内容提取的 Jina AI 阅读器工具 |
| `AgentMergeTools` | 将多个智能体工具合并为一个列表 |

### OpenAI 原生客户端
| 节点 | 描述 |
|------|-------------|
| `OpenAiNative` | 通用 OpenAI 客户端 |
| `OpenAiModelScope` | ModelScope API 客户端 |
| `OpenAiOpenRouter` | OpenRouter API 客户端 |
| `OpenAiHuggingFace` | Hugging Face 推理提供商客户端 |
| `OpenAiDeepSeek` | DeepSeek API 客户端 |
| `OpenAiDashScope` | 阿里巴巴 DashScope (Qwen) 客户端 |
| `OpenAiJinaAI` | Jina AI API 客户端 |
| `OpenAiNativeChat` | 支持视觉的聊天完成 |

### 文本生成图像
| 节点 | 描述 |
|------|-------------|
| `ModelScopeTextToImage` | 通过 ModelScope 生成图像（FLUX、Qwen-Image 等） |
| `HFTextToImage` | 通过 Hugging Face 推理提供商生成图像 |

### 图像编辑
| 节点 | 描述 |
|------|-------------|
| `OpenRouterImage` | 使用 OpenRouter 生成/编辑图像（Gemini、GPT-5-image） |
| `ModelScopeQwenImageEdit` | 通过 ModelScope 使用 Qwen-Image-Edit 编辑图像 |
| `SeedreamImage` | 使用字节跳动 Seedream 生成/编辑图像 |
| `HFImageToImage` | 通过 Hugging Face 推理提供商编辑图像 |

### 数据
| 节点 | 描述 |
|------|-------------|
| `DataFrameLoader` | 将 CSV 数据加载到 pandas DataFrame |
| `DatePicker` | 选择日期（字符串） |
| `TextFileLoader` | 从 ComfyUI 输入目录加载文本文件 |
| `TextSaver` | 将文本保存到输出目录的文件 |

### 金融
| 节点 | 描述 |
|------|-------------|
| `AKShareStockHistory` | 通过 AKShare 获取中国股票历史 |
| `AKShareMacroChinaCPI` | 获取中国 CPI 数据（年度/月度） |
| `AKShareMacroChinaPPI` | 获取中国 PPI 数据（年度） |
| `YfinanceTicker` | 从 Yahoo Finance 获取股票数据 |

### 可视化
| 节点 | 描述 |
|------|-------------|
| `MatplotlibVisualization` | 通过 AI 生成的 Matplotlib 代码生成静态图表 |
| `PlotlyVisualization` | 通过 AI 生成交互式 Plotly HTML 图表 |
| `BokehVisualization` | 通过 AI 生成交互式 Bokeh HTML 图表 |
| `MermaidChart` | 通过 AI 生成 Mermaid 图表 HTML |

### 显示
| 节点 | 描述 |
|------|-------------|
| `HTMLPreviewer` | 在 ComfyUI 中预览 HTML 字符串 |
| `HtmlIFramePreviewer` | 在 iframe 中预览 HTML/URL |
| `CodeViewer` | 查看带有语法高亮的代码 |
| `MarkDownViewer` | 预览 Markdown 内容 |

### 云存储
| 节点 | 描述 |
|------|-------------|
| `CloudflareR2` | 将图像上传到 Cloudflare R2 并获取公开 URL |

### 通用工具
| 节点 | 描述 |
|------|-------------|
| `JSONParse` | 将 JSON 字符串解析为字典 |
| `EmptyChatMessages` | 使用系统/用户提示词初始化聊天消息 |
| `PromptMerge` | 使用模板字符串合并提示词 |
| `MDConvert` | 将 Markdown 文本转换为 HTML |


## 配置与 API 密钥

大多数节点需要来自相应服务的 API 密钥。从以下位置获取密钥：

- **ModelScope**: [https://modelscope.cn](https://modelscope.cn)
- **Hugging Face 推理提供商**: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- **OpenRouter**: [https://openrouter.ai/keys](https://openrouter.ai/keys)
- **DeepSeek**: [https://platform.deepseek.com/api-keys](https://platform.deepseek.com/api-keys)
- **DashScope (Qwen)**: [https://dashscope.aliyun.com](https://dashscope.aliyun.com)
- **Jina AI**: [https://jina.ai/reader](https://jina.ai/reader)
- **Cloudflare R2**: [https://dash.cloudflare.com](https://dash.cloudflare.com)

请安全存储密钥；您可以直接在节点参数中输入它们，或者如果可用，使用 ComfyUI 的密钥管理功能。

## 许可证

本项目在 [CC BY-NC-SA 4.0 许可证](LICENSE) 下发布。

## 贡献

欢迎贡献！请在 GitHub 上提交 issue 或拉取请求。

## 支持

对于错误、功能请求或问题，请使用 [GitHub Issues](https://github.com/twn39/ComfyUI-AI-Toolkits/issues) 页面。

---

*本插件与任何提及的 API 提供商无关联。使用第三方服务受其各自条款和政策的约束。*