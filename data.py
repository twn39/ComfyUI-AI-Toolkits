import io
import os
import pandas as pd
from datetime import datetime
import folder_paths


class DataFrameLoader:
    # 定义节点的输入类型
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "csv_content": ("STRING", {"default": "", "multiline": True}),
                "has_header": ("BOOLEAN", {"default": True}),
                "encoding": ("STRING", {"default": "utf-8"}),
            },
            "optional": {
                "delimiter": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("DATA_FRAME", "STRING")
    RETURN_NAMES = ("df", "describe")
    FUNCTION = "load_pandas_data"
    CATEGORY = "AIToolkits/Data"

    OUTPUT_NODE = False

    @staticmethod
    def load_pandas_data(csv_content: str, has_header, encoding, delimiter=""):
        string_io_object = io.StringIO(csv_content)
        params = {}
        if delimiter != "":
            params["sep"] = delimiter
        if has_header:
            params["header"] = 0

        try:
            df = pd.read_csv(
                string_io_object,
                encoding=encoding,
                **params,
            )
            describe_text = df.describe().to_string()
            return df, describe_text
        except Exception as e:
            raise Exception(f"读取 CSV 文件时发生错误: {e}")


class DatePicker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "date": ("STRING", {"default": None, "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("date",)
    FUNCTION = "date_picker"
    CATEGORY = "AIToolkits/Data"

    @staticmethod
    def date_picker(date: str):
        return (date,)


class TextFileLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file": ("STRING", {"default": "No file selected", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "read_file_content"
    CATEGORY = "AIToolkits/Loaders"

    def read_file_content(self, file):
        if file == "No file selected":
            return ("",)

        # 使用 folder_paths 获取 ComfyUI 的 input 目录
        input_dir = folder_paths.get_input_directory()

        # 构建完整的文件路径
        file_path = os.path.join(input_dir, file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return (content,)
        except FileNotFoundError:
            raise Exception(
                f"Error: File not found at {file_path}",
            )
        except Exception as e:
            raise Exception(
                f"Error reading file: {e}",
            )


class TextSaver:
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "filename": ("STRING", {"default": "ComfyUI_Text"}),
                "file_extension": ("STRING", {"default": "txt"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)

    FUNCTION = "save_text_file"
    CATEGORY = "AIToolkits/Loaders"

    @staticmethod
    def save_text_file(text, filename: str, file_extension: str):
        output_dir = folder_paths.get_output_directory()

        text_output_dir = os.path.join(output_dir, "text_files")
        if not os.path.exists(text_output_dir):
            os.makedirs(text_output_dir)

        if file_extension.startswith("."):
            file_extension = file_extension[1:]

        desired_file_path = os.path.join(
            text_output_dir, f"{filename}.{file_extension}"
        )

        if os.path.exists(desired_file_path):
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            unique_filename = f"{filename}_{timestamp}.{file_extension}"
            full_file_path = os.path.join(text_output_dir, unique_filename)
        else:
            full_file_path = desired_file_path

        try:
            with open(full_file_path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            raise Exception(f"错误：无法保存文件 {full_file_path}。原因: {e}")

        return (full_file_path,)
