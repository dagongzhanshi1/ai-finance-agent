"""
Day 20 — 金融新闻摘要工具的核心模块

Day 24-26 更新：
- 加错误重试：API 失败自动重试 3 次 ✅
- 加缓存：相同文章不重复调 API ✅
- 加日志：记录每次调用的时间、cost、耗时 ✅

输入一段金融新闻文本，输出结构化摘要。
"""

import json
import time
from pydantic import BaseModel, Field
from config import get_client, get_model

# ============================================================
# 配置：重试参数
# ============================================================
MAX_RETRIES = 3            # 最多重试 3 次
RETRY_DELAY = 2            # 每次重试间隔 2 秒

# DeepSeek V4 Flash 价格（单位：元/1M tokens）
PRICE_PROMPT = 1.0
PRICE_COMPLETION = 2.0


class NewsSummary(BaseModel):
    """一条金融新闻的结构化摘要"""
    date: str = Field(description="新闻日期，如 2026-05-21")
    headline: str = Field(description="新闻标题，15字以内")
    summary: str = Field(description="100字以内的核心摘要")
    key_points: list[str] = Field(description="3-5个关键要点")
    sentiment: str = Field(description="情绪倾向：positive / negative / neutral")
    related_stocks: list[str] = Field(description="相关股票或公司，最多3个")


SYSTEM_PROMPT = """你是一个金融新闻分析助手。
你的任务是将输入的新闻文本提炼为结构化 JSON 数据。

请严格按以下 JSON 格式输出，不要加任何额外文字：

{
  "date": "新闻日期，如 2026-05-21",
  "headline": "简洁标题，不超过15个字",
  "summary": "核心摘要，不超过100字，包含事件和影响",
  "key_points": ["要点1", "要点2", "要点3", "要点4", "要点5"],
  "sentiment": "positive 或 negative 或 neutral",
  "related_stocks": ["相关公司或股票，最多3个，没有则填空数组"]
}"""


def build_user_prompt(text: str) -> str:
    """构造用户 prompt。"""
    return f"分析以下金融新闻，按要求的 JSON 格式输出：\n\n{text}"


def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    """根据 token 消耗算钱，返回人民币金额。"""
    return (prompt_tokens / 1_000_000 * PRICE_PROMPT +
            completion_tokens / 1_000_000 * PRICE_COMPLETION)


def summarize_news(text: str, cache=None) -> dict:
    """
    输入新闻文本 → 返回结构化摘要（字典格式）。

    支持：
    - 缓存：如果 cache 不为 None，查缓存，命中就不调 API
    - 重试：API 调用失败自动重试 3 次
    - 返回详情：包含结果 + cost + 耗时
    """
    # ========== 第一步：查缓存 ==========
    if cache is not None:
        cached = cache.get(text)
        if cached is not None:
            return {
                "result": cached,
                "from_cache": True,
                "cost": 0,
                "duration": 0,
                "tokens": 0,
            }

    # ========== 第二步：调 API（带重试） ==========
    client = get_client()
    model = get_model()
    start_time = time.time()

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_user_prompt(text)},
                ],
                temperature=0,
            )

            content = response.choices[0].message.content
            if content is None:
                raise ValueError("模型返回为空")

            # 解析 JSON
            raw = json.loads(content)

            # 用 Pydantic 校验
            summary = NewsSummary(**raw)
            duration = time.time() - start_time

            # 算花费
            u = response.usage
            cost = calculate_cost(u.prompt_tokens, u.completion_tokens)

            result_dict = summary.model_dump()

            # ========== 第三步：写入缓存 ==========
            if cache is not None:
                cache.set(text, result_dict, cost)

            return {
                "result": result_dict,
                "from_cache": False,
                "cost": cost,
                "duration": round(duration, 2),
                "tokens": u.total_tokens,
            }

        except (json.JSONDecodeError, ValueError) as e:
            # JSON 解析或数据校验失败 → 不重试，直接报错（重试也没用）
            raise e

        except Exception as e:
            # 网络错误、API 超时等 → 可以重试
            last_error = e
            if attempt < MAX_RETRIES:
                print(f"  ⚠️ API 调用失败（第{attempt}次），{RETRY_DELAY}秒后重试...")
                time.sleep(RETRY_DELAY)

    # 3 次都失败
    raise Exception(f"API 调用失败（已重试{MAX_RETRIES}次）: {last_error}")
