"""
Day 20 — 配置文件

统一管理 API key、base_url、model 名称。
方便切换 provider 时只改这一个文件。
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 从 .env 读 API key

# ============ 在这里切换 provider ============

# DeepSeek 配置
API_BASE_URL = "https://api.deepseek.com/v1"
MODEL_NAME = "deepseek-v4-flash"  # ← 更新到最新模型

# 如果你想切换到其他 provider，只需改上面两个变量：
# OpenAI:    API_BASE_URL="https://api.openai.com/v1",    MODEL_NAME="gpt-4o-mini"
# Gemini:    API_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai",  MODEL_NAME="gemini-2.5-flash"
# ===========================================

def get_client() -> OpenAI:
    """创建并返回 OpenAI 客户端（指向配置的 provider）"""
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=API_BASE_URL
    )

def get_model() -> str:
    """返回当前使用的模型名称"""
    return MODEL_NAME
