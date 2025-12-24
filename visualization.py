import textwrap
import pandas as pd
from openai import OpenAI
from agno.tools.python import PythonTools
from .utils import convert_base64_to_image, pil_image_to_tensor


vis_system_prompt = textwrap.dedent("""\
你是一个资深的 Python 软件工程师，擅长数据处理和可视化。

我需要你编写一个高质量的 Python 代码片段，该代码定义并执行一个函数，最终生成一个代表图表的 Base64 字符串。

**关键环境要求 (Critical Environment Requirement):**

*   由于 Seaborn 底层依赖于 Matplotlib，此代码将在一个**非 GUI、多线程的服务器环境**中执行。为了防止程序因尝试创建 GUI 窗口而崩溃，**必须**使用 Matplotlib 的非交互式后端。
*   你必须在导入 `matplotlib.pyplot` 或 `seaborn` 之前，通过 `matplotlib.use('Agg')` 来设置后端。
*   **封装**: 所有 `import` 语句 (如 `pandas`, `io`, `base64`) 都必须放在函数内部，以确保良好的封装性。

**详细功能规格 (Specifications):**

1.  **函数定义**:
    *   创建一个名为 `create_plot_as_base64` 的函数。
    *   函数签名应为 `def create_plot_as_base64(df: pd.DataFrame, title: str) -> str:`

2.  **核心逻辑与输出机制**:
    *   **关键要求 (封装与环境兼容性)**:
        1.  在函数内部，首先导入 `matplotlib` 并立即设置后端：`matplotlib.use('Agg')`。
        2.  然后，再导入 `matplotlib.pyplot as plt`, `seaborn as sns` 以及其他需要的模块 (`pandas`, `scipy`, `io`, `base64`)。
        3.  所有的依赖导入都必须放在函数内部以确保最大的稳定性和封装性。
    *   函数内部应使用 **Seaborn** 根据 `plot_type` 参数进行绘图 (例如 `sns.barplot`, `sns.lineplot` 等)。
    *   为图表设置标题。
    *   由于 Matplotlib 库对 CJK 字体支持不好，因此需要文本标注的地方一律使用英文
    *   使用 mplfinance 绘制股票数据
    *   将绘制的图表保存到内存中的二进制缓冲区 (`io.BytesIO`)。
    *   将缓冲区中的字节数据编码为 Base64 字符串并返回。
    *   在函数结束前，必须调用 `plt.close('all')` 来关闭图形，释放内存。

**执行与输出 (Execution & Output):**

*   在定义完 `create_plot_as_base64` 函数后，在代码末尾添加执行逻辑。
*   **核心假设**: 代码将在一个已存在名为 `df` 的 pandas DataFrame 对象的环境中执行。
*   **执行步骤**:
    1.  直接调用定义的函数，使用环境中已有的 `df` 变量。
    2.  将函数返回的 Base64 字符串赋值给一个名为 `result_image` 的变量。

**输出格式要求 (Output Format Requirements):**

*   你的回答必须是纯粹的 Python 代码，不要使用 Markdown 代码块 (```) 包裹。
*   除了关键代码注释外，不要有任何额外的解释。
*   你的输出将直接作为代码被执行，因此必须是干净、完整且可直接运行的 Python 脚本内容。 
*   代码风格必须严格遵守 PEP 8 规范，特别是：必须使用 4 个空格进行缩进，绝不能混用制表符 (Tab) 和空格，以避免 IndentationError。 \
""")


class MatplotlibVisualization:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "client": ("OPENAI_NATIVE_CLIENT",),
                "df": ("DATA_FRAME",),
                "task": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "model": ("STRING", {"multiline": False, "dynamicPrompts": False}),
                "temperature": (
                    "FLOAT",
                    {"default": 0.3, "min": 0, "max": 2, "step": 0.1},
                ),
                "max_tokens": (
                    "INT",
                    {"default": 4096, "min": 250, "max": 40960, "step": 1024},
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

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "code")
    FUNCTION = "run_matplotlib_visualization"
    CATEGORY = "AIToolkits/Visualization"

    @staticmethod
    def run_matplotlib_visualization(
        client: OpenAI,
        df: pd.DataFrame,
        task: str,
        model: str,
        temperature: float,
        max_tokens: int,
        seed: int = 0,
    ):
        df_cols = df.columns
        python_tool = PythonTools(safe_locals={"df": df}, safe_globals={"pd": pd})

        prompt = textwrap.dedent(f"""\
data value: df
df.describe:
{df.describe()}
df.columns:
{df_cols}

task:
{task}  \
""")

        messages = [
            {"role": "system", "content": vis_system_prompt},
            {"role": "user", "content": prompt},
        ]

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = completion.choices[0].message.content
        image_base64 = python_tool.run_python_code(
            code=content, variable_to_return="result_image"
        )
        if image_base64.startswith("Error running python code"):
            raise Exception(image_base64)

        pil_image = convert_base64_to_image(image_base64)
        image_tensor = pil_image_to_tensor(pil_image)

        return image_tensor, content


plotly_system_prompt = textwrap.dedent("""\
你是一个资深的 Python 数据科学家和软件工程师，尤其擅长使用 Plotly 进行交互式数据可视化。

我需要你编写一个高质量的 Python 函数，该函数接收一个 pandas DataFrame，并使用 Plotly Express 生成一个交互式图表的 HTML 字符串。

**详细功能规格 (Specifications):**

1.  **函数定义**:
    *   创建一个名为 `create_plotly_html` 的函数。
    *   函数签名应为 `def create_plotly_html(df: pd.DataFrame, title: str) -> str:`
    *   参数说明：
        *   `df`: 输入的 pandas DataFrame。
        *   `title`: 图表的标题。

2.  **核心逻辑与输出机制**:
    *   **封装**: 所有 `import` 语句 (如 `pandas`, `plotly.express`) 都必须放在函数内部，以确保良好的封装性。
    *   **绘图库**: 必须使用 `plotly.express` (别名 `px`) 来创建图表。
    *   **图表定制**: 使用传入的 `title` 参数设置图表的标题。可以适当添加一些通用的图表美化设置，例如更新布局模板。
    *   **输出格式**: 图表必须通过调用 `fig.to_html(full_html=False, include_plotlyjs='cdn')` 方法转换为 HTML 字符串。
        *   `full_html=False`: 确保只生成图表的 `<div>` 元素，而不是一个完整的 HTML 文档，使其更易于嵌入。
        *   `include_plotlyjs='cdn'`: 从 CDN 加载 Plotly.js 库，而不是将其内联到 HTML 中，这会使返回的字符串体积大大减小。
    *   **返回值**: 函数最终返回生成的 HTML 字符串。

**执行与输出 (Execution & Output):**

*   在函数定义之后，请提供一段示例代码来调用这个函数。
*   **核心假设**: 代码将在一个已存在名为 `df` 的 pandas DataFrame 对象的环境中执行。
*   **执行步骤**:
    1.  直接调用定义的函数，使用环境中已有的 `df` 变量。
    2.  将函数返回的 HTML 字符串赋值给一个名为 `chart_html` 的变量。

**输出格式要求 (Output Format Requirements):**

*   你的回答必须是纯粹的 Python 代码，不要使用 Markdown 代码块 (```) 包裹。
*   除了代码注释外，不要有任何额外的解释。
*   你的输出将直接作为代码被执行，因此必须是干净、完整且可直接运行的 Python 脚本内容。 
*   代码风格必须严格遵守 PEP 8 规范，特别是：必须使用 4 个空格进行缩进，绝不能混用制表符 (Tab) 和空格，以避免 IndentationError。 \
""")


class PlotlyVisualization:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "client": ("OPENAI_NATIVE_CLIENT",),
                "df": ("DATA_FRAME",),
                "task": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "model": ("STRING", {"multiline": False, "dynamicPrompts": False}),
                "temperature": (
                    "FLOAT",
                    {"default": 0.3, "min": 0, "max": 2, "step": 0.1},
                ),
                "max_tokens": (
                    "INT",
                    {"default": 4096, "min": 250, "max": 40960, "step": 1024},
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

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("html", "code")
    FUNCTION = "run_plotly_visualization"
    CATEGORY = "AIToolkits/Visualization"

    @staticmethod
    def run_plotly_visualization(
        client: OpenAI,
        df: pd.DataFrame,
        task: str,
        model: str,
        temperature: float,
        max_tokens: int,
        seed: int = 0,
    ):
        df_cols = df.columns
        python_tool = PythonTools(safe_locals={"df": df}, safe_globals={"pd": pd})

        prompt = textwrap.dedent(f"""\
data value: df
df.describe:
{df.describe()}
df.columns:
{df_cols}

task:
{task}  \
""")

        messages = [
            {"role": "system", "content": plotly_system_prompt},
            {"role": "user", "content": prompt},
        ]

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = completion.choices[0].message.content
        html = python_tool.run_python_code(
            code=content, variable_to_return="chart_html"
        )
        if html.startswith("Error running python code"):
            raise Exception(html)

        return html, content


bokeh_system_prompt = textwrap.dedent('''\
你是一个资深的 Python 数据科学家和软件工程师，尤其擅长使用 Bokeh 进行交互式数据可视化。

我需要你编写一个高质量的 Python 函数，该函数接收一个 pandas DataFrame，并使用 Bokeh 生成一个**完全自包含、可直接嵌入**的交互式图表的 HTML 字符串。

**详细功能规格 (Specifications):**

1.  **函数定义**:
    *   创建一个名为 `create_bokeh_html` 的函数。
    *   函数签名应为 `def create_bokeh_html(df: pd.DataFrame, title: str) -> str:`
    *   参数说明：
        *   `df`: 输入的 pandas DataFrame。
        *   `title`: 图表的标题。

2.  **核心逻辑与输出机制**:
    *   **封装**: 所有 `import` 语句 (如 `pandas`, `bokeh`, `math`, ...) 都必须放在函数内部，以确保良好的封装性。
    *   **绘图库**: 必须使用 `bokeh.plotting` 中的 `figure` 函数来创建图表。
    *   **图表定制**: 使用传入的 `title` 参数设置图表的标题。
    *   **输出格式**: 函数必须生成一个包含了所有依赖的、自包含的 HTML 字符串。这需要组合以下几个部分：
        1.  **BokehJS 库**: 使用 `bokeh.resources.CDN.render()` 来生成从 CDN 加载 BokehJS 库和相关 CSS 的 `<script>` 和 `<link>` 标签。
        2.  **图表组件**: 使用 `bokeh.embed.components(p, CDN)` 来生成图表本身的 `<script>` 和 `<div>` 元素。
        3.  **组合**: 将上述生成的 CDN 链接、图表脚本和图表 `<div>` 拼接成一个完整的、可独立工作的 HTML 字符串。
    *   **返回值**: 函数最终返回这个拼接好的、自包含的 HTML 字符串。
    
    > 注意事项：
        1. 请确保 DatetimeTickFormatter 的 hours, days, months, years 等参数接收的是字符串格式（例如 '%Y-%m-%d'），而不是列表。
        2. 在 Bokeh 中，ColumnDataSource 不支持像 pandas DataFrame 那样直接使用布尔索引进行过滤（例如 source[inc] 会报错）。正确的、推荐的做法是使用 bokeh.models.CDSView 和 bokeh.models.BooleanFilter 来创建数据的视图。这样可以避免创建多个数据源，提高效率。
    
    示例：
    ```
    # 生成HTML
    script, div = bokeh.embed.components(fig, CDN)
    cdn_links = bokeh.resources.CDN.render()

    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            {cdn_links}
        </head>
        <body>
            {div}
            {script}
        </body>
    </html>
    """
    ```

**执行与输出 (Execution & Output):**

*   在函数定义之后，请提供一段示例代码来调用这个函数。
*   **核心假设**: 代码将在一个已存在名为 `df` 的 pandas DataFrame 对象的环境中执行。
*   **执行步骤**:
    1.  直接调用定义的函数，使用环境中已有的 `df` 变量。
    2.  将函数返回的 HTML 字符串赋值给一个名为 `chart_html` 的变量。

**输出格式要求 (Output Format Requirements):**

*   你的回答必须是纯粹的 Python 代码，不要使用 Markdown 代码块 (```) 包裹。
*   除了代码注释外，不要有任何额外的解释。
*   你的输出将直接作为代码被执行，因此必须是干净、完整且可直接运行的 Python 脚本内容。 
*   代码风格必须严格遵守 PEP 8 规范，特别是：必须使用 4 个空格进行缩进，绝不能混用制表符 (Tab) 和空格，以避免 IndentationError。 \
''')


class BokehVisualization:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "client": ("OPENAI_NATIVE_CLIENT",),
                "df": ("DATA_FRAME",),
                "task": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "model": ("STRING", {"multiline": False, "dynamicPrompts": False}),
                "temperature": (
                    "FLOAT",
                    {"default": 0.3, "min": 0, "max": 2, "step": 0.1},
                ),
                "max_tokens": (
                    "INT",
                    {"default": 4096, "min": 250, "max": 40960, "step": 1024},
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

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("html", "code")
    FUNCTION = "run_bokeh_visualization"
    CATEGORY = "AIToolkits/Visualization"

    @staticmethod
    def run_bokeh_visualization(
        client: OpenAI,
        df: pd.DataFrame,
        task: str,
        model: str,
        temperature: float,
        max_tokens: int,
        seed: int = 0,
    ):
        df_cols = df.columns
        python_tool = PythonTools(safe_locals={"df": df}, safe_globals={"pd": pd})

        prompt = textwrap.dedent(f"""\
data value: df
df.describe:
{df.describe()}
df.columns:
{df_cols}

task:
{task}  \
""")

        messages = [
            {"role": "system", "content": bokeh_system_prompt},
            {"role": "user", "content": prompt},
        ]

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = completion.choices[0].message.content
        html = python_tool.run_python_code(
            code=content, variable_to_return="chart_html"
        )
        if html.startswith("Error running python code"):
            raise Exception(html)

        return html, content


mermaid_system_prompt = textwrap.dedent("""\
你是一位精通 Mermaid 语法的专家。你的任务是根据我提供的描述，生成一段严格符合 Mermaid 格式的代码。

这段代码将用于通过 Mermaid CLI 直接转换为 SVG 图像，因此必须满足以下要求：
1.  只输出一个 Mermaid 代码块。
2.  你的回答必须是纯粹的 Mermaid 代码，不要使用 Markdown 代码块 (```) 包裹。
3   你的输出将直接作为 Mermaid CLI 的输入内容，因此必须是干净、完整且可转换的 Mermaid 内容。 
4.  代码块内只包含纯粹的 Mermaid 语法，不要有任何额外的解释、标题或注释。
5.  确保语法是完整且无误的。 \
""")


class MermaidChart:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "client": ("OPENAI_NATIVE_CLIENT",),
                "task": ("STRING", {"multiline": True, "dynamicPrompts": False}),
                "model": ("STRING", {"multiline": False, "dynamicPrompts": False}),
                "temperature": (
                    "FLOAT",
                    {"default": 0.3, "min": 0, "max": 2, "step": 0.1},
                ),
                "max_tokens": (
                    "INT",
                    {"default": 4096, "min": 250, "max": 40960, "step": 1024},
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

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("html", "code")
    FUNCTION = "run_mermaid_chart"
    CATEGORY = "AIToolkits/Visualization"

    @staticmethod
    def run_mermaid_chart(
        client: OpenAI,
        task: str,
        model: str,
        temperature: float,
        max_tokens: int,
        seed: int = 0,
    ):
        messages = [
            {"role": "system", "content": mermaid_system_prompt},
            {"role": "user", "content": task},
        ]

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = completion.choices[0].message.content

        html_content = f'''
<!doctype html>
<html lang="en">
  <body>
    <pre class="mermaid">
{content}
    </pre>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    </script>
  </body>
</html>
        '''

        return html_content, content
