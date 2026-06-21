# AI Finance Portfolio

面向 AI + Finance 求职的阶段式作品集。这个仓库不是零散工具集合，而是一条从金融数据分析到 LLM 应用、再到 RAG 金融文档问答系统的学习和项目主线。

## Portfolio Overview

| 阶段 | 项目 | 核心能力 | 产出形态 | 状态 |
|---|---|---|---|---|
| 1 | [股票收益率与风险分析](./01-stock-analysis/) | Python、Pandas、SQL、金融指标、可视化 | 数据分析脚本 + 图表输出 | 已完成 |
| 2 | [金融新闻摘要工具](./02-news-summarizer/) | LLM API、Prompt、结构化输出、缓存、CLI | 命令行摘要工具 | 已完成 |
| 3 | [金融文档 RAG 问答系统](./03-financial-rag/) | PDF 解析、Embedding、Chroma、RAG、Streamlit | Web 问答应用 | 已完成 |

> 阶段 2 的新闻摘要工具保留为本仓库第二阶段项目，不再作为独立作品集主页项目单独展示。

## Repository Structure

```text
ai-finance-portfolio/
├── 01-stock-analysis/        # 阶段 1：股票数据分析与风险指标
├── 02-news-summarizer/       # 阶段 2：LLM 金融新闻摘要工具
├── 03-financial-rag/         # 阶段 3：金融文档 RAG 问答系统
├── 04-finance-agent/         # 后续阶段：金融 Agent 原型
├── requirements.txt          # 阶段 1-3 公共依赖
├── verify_setup.py           # 环境检查脚本
└── README.md
```

## Project 1: 股票收益率与风险分析

目标：用 Python 完成一套基础金融数据分析流程，从数据获取到风险收益指标计算，再到图表展示。

主要内容：

- 使用 `yfinance` 下载股票历史行情
- 用 Pandas 处理价格、收益率和多股票数据
- 计算年化收益率、年化波动率、最大回撤、夏普比率
- 绘制累计净值曲线、相关性热力图和行业对比图
- 使用 SQLite 做基础 SQL 查询练习

运行示例：

```bash
python3 01-stock-analysis/08-download.py
python3 01-stock-analysis/09-analyze.py
python3 01-stock-analysis/10-visualize.py
```

## Project 2: 金融新闻摘要工具

目标：把 LLM API 调用包装成一个可复用的金融新闻摘要 CLI 工具，而不是只停留在单次 API 示例。

主要内容：

- 调用 DeepSeek OpenAI-compatible API
- 通过 Prompt 约束 JSON 输出
- 使用 Pydantic 校验结构化结果
- 支持交互输入、管道输入、单文件、多文件和目录批处理
- 使用 MD5 本地缓存避免重复调用
- 记录调用日志、token 数、耗时和成本

运行示例：

```bash
cd 02-news-summarizer
pip install -r requirements.txt
cp .env.example .env

python3 main.py articles/01-ashare.txt
python3 main.py --dir ./articles/
python3 main.py --log
```

## Project 3: 金融文档 RAG 问答系统

目标：做一个可以上传金融 PDF、检索原文片段并生成带来源回答的 RAG 应用。

主要内容：

- 使用 `pdfplumber` 提取年报 / 研报文本
- 使用 `RecursiveCharacterTextSplitter` 切分文本
- 使用 `BAAI/bge-small-zh-v1.5` 生成本地 embedding
- 使用 ChromaDB 持久化向量库
- 调用 DeepSeek 基于检索上下文生成回答
- 使用 Streamlit 提供聊天界面、引用来源和 Markdown 导出

运行示例：

```bash
cd 03-financial-rag
pip install -r requirements.txt
cp .env.example .env

streamlit run app.py
```

浏览器打开 `http://localhost:8501`。

## Quick Start

建议使用 Python 3.10+。

```bash
git clone https://github.com/dagongzhanshi1/ai-finance-portfolio.git
cd ai-finance-portfolio

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
- Python 缓存、数据库文件和图片输出

## Learning Notes

这个仓库的核心价值不是单个脚本，而是三个阶段能力的递进：

```text
金融数据分析
  -> LLM 结构化处理金融文本
  -> RAG 检索金融文档并生成可追溯回答
```

后续阶段会在 `04-finance-agent/` 中继续扩展金融 Agent，但当前 GitHub 主页重点展示前 3 个已完成项目。
