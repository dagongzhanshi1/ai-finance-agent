"""
Day 24 — 文件持久化缓存

把之前调 API 的结果存到文件里，相同的文章不再重复调用。
"""

import json
import hashlib
import os
from datetime import datetime

CACHE_FILE = os.path.join(os.path.dirname(__file__), ".summary_cache.json")


class Cache:
    """文件持久化缓存。key = 文章内容的 MD5 哈希，value = 摘要结果。"""

    def __init__(self, file_path=None):
        self.file_path = file_path or CACHE_FILE
        self.data = self._load()

    def _load(self) -> dict:
        """从文件加载缓存。文件不存在就返回空字典。"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save(self):
        """把缓存写回文件。"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def _make_key(self, text: str) -> str:
        """把文章内容转成固定长度的哈希值，作为缓存 key。"""
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def get(self, text: str):
        """查缓存：有就返回结果，没有返回 None。"""
        key = self._make_key(text)
        entry = self.data.get(key)
        if entry is None:
            return None
        return entry["result"]

    def set(self, text: str, result: dict, cost: float = 0):
        """写入缓存：存结果 + 时间戳 + 花费。"""
        key = self._make_key(text)
        self.data[key] = {
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "cost": cost,
        }
        self._save()

    def stats(self) -> dict:
        """返回缓存统计信息。"""
        return {
            "总缓存条数": len(self.data),
            "缓存文件": self.file_path,
        }
