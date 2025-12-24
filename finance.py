import yfinance as yf
import akshare as ak
from dateutil.parser import parse


class YfinanceTicker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ticker": ("STRING", {"default": None, "multiline": False}),
                "start": ("STRING", {"default": None, "multiline": False}),
                "end": ("STRING", {"default": None, "multiline": False}),
                "interval": (
                    ["1h", "4h", "1d", "5d", "1wk", "1mo", "3mo"],
                    {"default": "1d"},
                ),
            },
        }

    RETURN_TYPES = ("DATA_FRAME",)
    RETURN_NAMES = ("df",)
    FUNCTION = "yfinance_tocker"
    CATEGORY = "AIToolkits/Finance"

    @staticmethod
    def yfinance_tocker(ticker: str, start: str, end: str, interval: str):
        data = yf.Ticker(ticker)
        df = data.history(start=start, end=end, interval=interval)
        return (df,)


class AKShareMacroChinaPPI:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "period": (["yearly"], {"default": "yearly"}),
            },
        }

    RETURN_TYPES = ("DATA_FRAME",)
    RETURN_NAMES = ("df",)
    FUNCTION = "akshare_macro_china_ppi"
    CATEGORY = "AIToolkits/Finance"

    @staticmethod
    def akshare_macro_china_ppi(period: str):
        df = ak.macro_china_ppi_yearly()
        return (df,)


class AKShareMacroChinaCPI:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "period": (["yearly", "monthly"], {"default": "monthly"}),
            },
        }

    RETURN_TYPES = ("DATA_FRAME",)
    RETURN_NAMES = ("df",)
    FUNCTION = "akshare_macro_china_cpi"
    CATEGORY = "AIToolkits/Finance"

    @staticmethod
    def akshare_macro_china_cpi(period: str):
        if period == "yearly":
            df = ak.macro_china_cpi_yearly()
        else:
            df = ak.macro_china_cpi_monthly()
        return (df,)


class AKShareStockHistory:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "symbol": ("STRING", {"multiline": False}),
                "period": (["daily", "weekly", "monthly"], {"default": "daily"}),
                "start_date": ("STRING", {"multiline": False}),
                "end_date": ("STRING", {"multiline": False}),
            },
        }

    RETURN_TYPES = ("DATA_FRAME",)
    RETURN_NAMES = ("stock",)
    FUNCTION = "akshare_zh_a_hist"
    CATEGORY = "AIToolkits/Finance"

    @staticmethod
    def akshare_zh_a_hist(symbol: str, period: str, start_date: str, end_date: str):
        start_date = parse(start_date)
        end_date = parse(end_date)
        stock_zh_a_hist_df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period,
            start_date=start_date.strftime("%Y%m%d"),
            end_date=end_date.strftime("%Y%m%d"),
        )
        return (stock_zh_a_hist_df,)
