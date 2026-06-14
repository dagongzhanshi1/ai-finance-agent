"""
Day 20 — 工具函数

Day 24-26 更新：
- 加日志记录：每次调用记下时间、文章标题、cost、耗时 ✅
- 加批量结果格式化 ✅
"""

import json
import os
from datetime import datetime
from summarizer import NewsSummary

LOG_FILE = os.path.join(os.path.dirname(__file__), "call_log.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def format_summary(summary: NewsSummary) -> str:
    """把 NewsSummary 对象格式化成终端可读的文本"""
    sentiment_icons = {
        "positive": "📈 正面",
        "negative": "📉 负面",
        "neutral": "➡️ 中性",
    }

    lines = [
        "=" * 50,
        f"📰 {summary.headline}",
        "=" * 50,
        f"📅 日期:     {summary.date}",
        f"💬 情绪:     {sentiment_icons.get(summary.sentiment, summary.sentiment)}",
        "",
        "📝 摘要:",
        f"   {summary.summary}",
        "",
        "🔑 关键要点:",
    ]

    for i, point in enumerate(summary.key_points, 1):
        lines.append(f"   {i}. {point}")

    if summary.related_stocks:
        lines.append("")
        lines.append(f"🏢 相关公司: {', '.join(summary.related_stocks)}")

    lines.append("=" * 50)
    return "\n".join(lines)


def save_summary(summary: NewsSummary, file_path: str = None) -> str:
    """把摘要保存为 JSON 文件，返回文件路径"""
    if file_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        file_path = os.path.join(OUTPUT_DIR, f"news_summary_{timestamp}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(summary.model_dump(), f, ensure_ascii=False, indent=2)

    return file_path


def format_batch_result(meta: dict) -> str:
    """格式化单篇文章的处理结果（含 cost 和耗时信息）"""
    lines = [f"  耗时: {meta['duration']}秒"]
    if meta.get("from_cache"):
        lines.append("  💾 缓存命中（免费）")
    else:
        lines.append(f"  💰 花费: ¥{meta['cost']:.6f}  |  tokens: {meta['tokens']}")
    return "\n".join(lines)


def log_call(source: str, meta: dict):
    """
    记录一次 API 调用日志到 CSV 文件。

    记录内容：时间、来源、是否缓存命中、cost、耗时、token数。
    """
    is_new_file = not os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        # 如果文件不存在，先写表头
        if is_new_file:
            f.write("时间,来源,缓存命中,cost(元),耗时(秒),token数\n")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cache_hit = "是" if meta.get("from_cache") else "否"
        cost = meta.get("cost", 0)
        duration = meta.get("duration", 0)
        tokens = meta.get("tokens", 0)

        f.write(f"{timestamp},{source},{cache_hit},{cost},{duration},{tokens}\n")


def read_log(lines: int = 10) -> str:
    """读取最近 N 行日志。"""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
            # 表头 + 最近 lines 行
            last_lines = all_lines[:1] + all_lines[-lines:]
            return "".join(last_lines)
    except FileNotFoundError:
        return "暂无日志记录\n"
