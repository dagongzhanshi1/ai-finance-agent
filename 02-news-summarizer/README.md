# Project 2: 金融新闻摘要工具

阶段 2 项目，目标是把 LLM API 调用做成一个可复用的金融新闻摘要 CLI 工具。它不是独立作品集主页项目，而是 `ai-finance-lab` 的第二阶段。

## What It Does

输入一篇或多篇金融新闻文本，调用 DeepSeek API，输出结构化 JSON 摘要。

核心能力：

- DeepSeek OpenAI-compatible API 调用
- Prompt 约束 JSON 输出
- Pydantic 校验字段类型
- 支持交互输入、管道输入、单文件、多文件、目录批处理
- 相同文章使用 MD5 本地缓存，避免重复调用 API
- 记录调用日志：时间、来源、缓存命中、成本、耗时、token 数
- 自动保存 JSON 结果到 `output/`

## Structure

```text
02-news-summarizer/
├── 01-first-call.py               # 第一次 API 调用
├── 02-prompt-lab.py               # Prompt 对比实验
├── 03-structured-output.py        # JSON 结构化输出
├── 03-structured-output-practice.py
├── 04-function-calling.py         # Function Calling 示例
├── 05-multi-turn-conversation.py  # 多轮对话历史
├── 06-cost-control.py             # token 成本控制
├── articles/                      # 测试新闻文本
├── output/                        # JSON 输出目录
├── cache.py                       # 本地缓存
├── config.py                      # API base_url / model 配置
├── main.py                        # CLI 入口
├── summarizer.py                  # 摘要核心逻辑
├── utils.py                       # 输出、保存、日志工具
├── requirements.txt
└── .env.example
```

## Setup

```bash
cd 02-news-summarizer
pip install -r requirements.txt
cp .env.example .env
```

把 `.env` 中的 `DEEPSEEK_API_KEY` 改成自己的 key。

## Usage

```bash
# 交互模式：粘贴新闻文本，按 Ctrl+D 结束
python3 main.py

# 单文件
python3 main.py articles/01-ashare.txt

# 多文件
python3 main.py articles/01-ashare.txt articles/02-tech-ai.txt

# 目录批处理
python3 main.py --dir ./articles/

# 管道输入
cat articles/01-ashare.txt | python3 main.py

# 查看最近调用日志
python3 main.py --log
```

## Output Schema

```json
{
  "date": "新闻日期",
  "headline": "简洁标题",
  "summary": "核心摘要",
  "key_points": ["关键要点"],
  "sentiment": "positive / negative / neutral",
  "related_stocks": ["相关公司或股票"]
}
```

## Portfolio Value

这个项目展示的是 LLM 应用开发能力：API 调用、Prompt 设计、结构化输出、Pydantic 校验、缓存和 CLI 工具封装。
