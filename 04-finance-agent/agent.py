"""agent.py - 金融助手 Agent，基于 DeepSeek Function Calling"""
import json
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from tool_schemas import tools
from scripts.stock_tools import (
    get_stock_price, get_pe_ratio, get_company_info,
    get_stock_change, get_volume, get_52week_range,
    get_financial_metrics, search_news,
)

load_dotenv()  # 从 .env 读 API key

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)

# 工具名字 -> 实际函数 的映射表
TOOL_MAP = {
    "get_stock_price": get_stock_price,
    "get_pe_ratio": get_pe_ratio,
    "get_company_info": get_company_info,
    "get_stock_change": get_stock_change,
    "get_volume": get_volume,
    "get_52week_range": get_52week_range,
    "get_financial_metrics": get_financial_metrics,
    "search_news": search_news,
}


def run_agent(user_input, max_iterations=5):
    messages = [
        {"role": "system", "content": "你是一个金融数据助手。根据用户的问题调用对应的工具来获取数据，然后用数据回答用户。"},
        {"role": "user", "content": user_input},
    ]

    for round_num in range(max_iterations):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )
        except Exception as e:
            return f"API 调用失败: {type(e).__name__}: {e}\n请检查网络连接或 API Key 是否有效。"

        msg = response.choices[0].message
        messages.append(msg)

        # LLM 直接回答了，没调工具 → 结束
        if not msg.tool_calls:
            return msg.content

        # LLM 调了工具 → 逐个执行
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name

            # 1️⃣ 参数解析失败（LLM 返回了不合法的 JSON）
            try:
                func_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"参数解析失败: {tool_call.function.arguments}",
                })
                continue

            # 2️⃣ 调了不存在的工具
            if func_name not in TOOL_MAP:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"未知工具: {func_name}，可用工具: {', '.join(TOOL_MAP.keys())}",
                })
                continue

            print(f"  → 调用工具: {func_name}({func_args})")

            # 3️⃣ 工具执行异常（网络超时、股票代码不存在等）
            try:
                func = TOOL_MAP[func_name]
                result = func(**func_args)
            except Exception as e:
                result = f"工具执行失败: {type(e).__name__}: {e}"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    # 4️⃣ 超过最大迭代次数，防止无限循环
    return "已达到最大迭代次数，请简化你的问题。"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("你想查什么？")
    print("查询中...")
    result = run_agent(user_input)
    print(result)
