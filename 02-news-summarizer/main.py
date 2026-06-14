"""
Day 20 — 金融新闻摘要工具 CLI 入口

Day 24-26 更新：
- 加批量处理：支持多个文件和目录 ✅
- 加缓存：相同的文章不重复调 API ✅
- 加日志：每次调用记下时间、来源、cost、耗时 ✅

用法：
  # 单文件
  python3 main.py news.txt

  # 多文件
  python3 main.py news1.txt news2.txt news3.txt

  # 目录（处理所有 .txt 文件）
  python3 main.py --dir ./articles/

  # 管道模式
  curl -s https://... | python3 main.py

  # 交互模式
  python3 main.py

  # 查看日志
  python3 main.py --log
  python3 main.py --log 20    # 看最近 20 条
"""

import sys
import json
import os

from summarizer import summarize_news, NewsSummary
from utils import format_summary, save_summary, format_batch_result, log_call, read_log
from cache import Cache


def process_single(text: str, source: str, cache: Cache, save_json: bool = True) -> dict:
    """处理单篇文章：查缓存 → 调 API → 存 JSON → 记录日志。返回 meta 信息。"""
    print(f"\n📥 正在分析 {source}...")
    print(f"📊 文本长度: {len(text)} 字符")

    try:
        meta = summarize_news(text, cache=cache)

        # 构造 NewsSummary 对象用于格式化
        summary = NewsSummary(**meta["result"])

        # 输出
        print(format_summary(summary))

        # 保存 JSON
        if save_json and not meta.get("from_cache"):
            saved_path = save_summary(summary)
            print(f"\n💾 JSON 已保存: {saved_path}")

        # 显示 cost 和耗时
        print(format_batch_result(meta))

        # 记录日志
        log_call(source, meta)

        return meta

    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        print("模型返回的不是有效 JSON。")
        return None
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        return None


def process_files(file_paths: list[str], cache: Cache):
    """批量处理多个文件。"""
    print(f"📂 共 {len(file_paths)} 个文件\n" + "=" * 50)

    total_cost = 0
    success = 0
    cache_hits = 0

    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(   f"\n⚠️ 文件不存在: {file_path}")
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
        except Exception as e:
            print(f"\n⚠️ 读取失败 {file_path}: {e}")
            continue

        if not text:
            print(f"\n⚠️ 空文件: {file_path}")
            continue

        meta = process_single(text, f"文件: {os.path.basename(file_path)}", cache)

        if meta is not None:
            success += 1
            total_cost += meta.get("cost", 0)
            if meta.get("from_cache"):
                cache_hits += 1

            print("-" *  50)

    # 汇总
    print(f"\n{'=' * 50}")
    print(f"📊 批量处理完成")
    print(f"   成功: {success}/{len(file_paths)}")
    print(f"   缓存命中: {cache_hits}")
    print(f"   总花费: ¥{total_cost:.6f}")


def process_directory(dir_path: str, cache: Cache):
    """处理目录下所有 .txt 文件。"""
    if not os.path.isdir(dir_path):
        print(f"❌ 目录不存在: {dir_path}")
        sys.exit(1)

    txt_files = sorted([
        os.path.join(dir_path, f)
        for f in os.listdir(dir_path)
        if f.endswith(".txt")
    ])

    if not txt_files:
        print(f"⚠️ 目录中没有 .txt 文件: {dir_path}")
        return

    process_files(txt_files, cache)


def main():
    cache = Cache()

    # ========== 解析参数 ==========

    # --log 模式：只看日志
    if "--log" in sys.argv:
        idx = sys.argv.index("--log")
        n = int(sys.argv[idx + 1]) if idx + 1 < len(sys.argv) and sys.argv[idx + 1].isdigit() else 10
        print(read_log(n))
        return

    # --dir 模式：处理目录
    if "--dir" in sys.argv:
        idx = sys.argv.index("--dir")
        if idx + 1 < len(sys.argv):
            process_directory(sys.argv[idx + 1], cache)
            return
        else:
            print("❌ 请指定目录路径，如: python3 main.py --dir ./articles/")
            sys.exit(1)

    # 多个文件
    if len(sys.argv) > 1:
        # 过滤掉 --dir 等参数（上面已经 return 了，这里都是纯文件路径）
        file_paths = [a for a in sys.argv[1:] if not a.startswith("--")]
        process_files(file_paths, cache)
        return

    # 管道模式
    if not sys.stdin.isatty():
        text = sys.stdin.read().strip()
        if text:
            source = "管道输入"
            meta = process_single(text, source, cache)
            if meta is None:
                sys.exit(1)
            return

    # 交互模式
    print("📰 金融新闻摘要工具（带缓存 + 日志）")
    print("粘贴新闻文本，按 Ctrl+D (macOS/Linux) 结束：")
    print("=" * 50)
    text = sys.stdin.read().strip()
    if not text:
        print("❌ 没有输入任何文本")
        sys.exit(1)

    meta = process_single(text, "键盘输入", cache)


if __name__ == "__main__":
    main()
