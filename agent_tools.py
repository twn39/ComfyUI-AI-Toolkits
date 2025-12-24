import numexpr as ne
from agno.tools import tool


@tool(show_result=True, stop_after_tool_call=True)
def math_expr(math_express: str) -> str:
    """
    Runs a math express and returns the calculated result.

    Args:
        math_express (str): The math expression to evaluate.
    Returns:
        str: The calculated result.
    """
    result = ne.evaluate(math_express)
    return f"{result}"

