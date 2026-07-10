# AI Finance Agent

面向 AI + Finance 求职的阶段式作品集——从金融数据分析到 LLM 应用、RAG 文档问答、再到 LangGraph 多步 Agent 工作流。

## Portfolio Overview

| 阶段 | 项目 | 核心能力 | 状态 |
|------|------|---------|------|
| 1 | [股票收益率与风险分析](./01-stock-analysis/) | Python、Pandas、金融指标、可视化 | ✅ |
| 2 | [金融新闻摘要工具](./02-news-summarizer/) | LLM API、Prompt 工程、结构化输出、缓存 | ✅ |
| 3 | [金融文档 RAG 问答系统](./03-financial-rag/) | PDF 解析、Embedding、Chroma、Streamlit | ✅ |
| 4 | [金融 Agent 工作流](./04-finance-agent/) | LangGraph、@tool、Supervisor Agent、MCP | ✅ |

## Repository Structure

```text
ai-finance-agent/
├── 01-stock-analysis/        # 阶段 1：股票数据分析与风险指标
├── 02-news-summarizer/       # 阶段 2：LLM 金融新闻摘要工具
├── 03-financial-rag/         # 阶段 3：金融文档 RAG 问答系统
├── 04-finance-agent/         # 阶段 4：LangGraph 金融 Agent 工作流
│   ├── workflow.py           # LangGraph 工作流（查行情→查财务→搜新闻→LLM报告）
│   ├── cli.py                # 命令行入口
│   ├── app.py                # Streamlit Web 界面
│   ├── tools_def.py          # @tool 工具定义
│   ├── supervisor_agent.py   # Supervisor Agent 模式
│   ├── mcp_stock_server.py   # MCP 股票查询服务器
│   ├── README.md
│   └── .gitignore
├── requirements.txt
├── README.md
└── verify_setup.py
```

## Project 1: 股票收益率与风险分析

目标：用 Python 完成一套基础金融数据分析流程，从数据获取到风险收益指标计算，再到图表展示。

```bash
python3 01-stock-analysis/08-download.py
python3 01-stock-analysis/09-analyze.py
python3 01-stock-analysis/10-visualize.py
```

## Project 2: 金融新闻摘要工具

目标：把 LLM API 调用包装成一个可复用的金融新闻摘要 CLI 工具。

```bash
cd 02-news-summarizer
python3 main.py articles/01-ashare.txt
python3 main.py --dir ./articles/
```

## Project 3: 金融文档 RAG 问答系统

目标：上传金融 PDF，检索原文片段并生成带来源回答的 RAG 应用。

```bash
cd 03-financial-rag
streamlit run app.py
```

## Project 4: 金融 Agent 工作流

目标：用 LangGraph 构建多步金融分析 Agent，支持 Supervisor 模式和 MCP 协议扩展。

```bash
cd 04-finance-agent

# 命令行：直接查股票
python cli.py 600519

# Streamlit Web 界面
streamlit run app.py

# Supervisor Agent 模式
python supervisor_agent.py 查一下茅台

# MCP 服务器（供 Hermes / Claude Code 等客户端连接）
python mcp_stock_server.py
```

## Quick Start

建议使用 Python 3.10+。

```bash
git clone https://github.com/dagongzhanshi1/ai-finance-agent.git
cd ai-finance-agent

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python3 verify_setup.py
```

需要调用 DeepSeek API 的阶段，先配置 `.env`：

```bash
cp 02-news-summarizer/.env.example 02-news-summarizer/.env
cp 03-financial-rag/.env.example 03-financial-rag/.env
```

然后在 `.env` 中填写：

```text
DEEPSEEK_API_KEY=your_api_key_here
```

## Data And Secrets

以下内容不会提交到 GitHub：

- `.env` API 密钥文件
- ChromaDB 本地数据库
- 大体积 PDF 年报和研报
- 运行生成的缓存、日志、JSON 输出
- 学习调试文件

## Learning Path

```text
金融数据分析（Pandas）
  → LLM 处理金融文本（API + Prompt）
  → RAG 检索金融文档（Chroma + Embedding）
  → Agent 多步工作流（LangGraph + Supervisor + MCP）
```
