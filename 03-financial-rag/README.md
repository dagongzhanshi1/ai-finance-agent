# Project 3: 金融文档 RAG 问答系统

阶段 3 核心项目。用户上传 PDF 年报或研报后，系统会提取文本、切分 chunk、写入 Chroma 向量库，并基于检索到的原文片段调用 DeepSeek 生成回答。

## What It Does

- PDF 年报 / 研报上传
- `pdfplumber` 文本提取
- `RecursiveCharacterTextSplitter` 文本切分
- 本地 `BAAI/bge-small-zh-v1.5` embedding
- ChromaDB 本地持久化
- DeepSeek OpenAI-compatible API 生成回答
- Streamlit 聊天式界面
- 引用来源展开查看
- 文档库选择、重命名、删除
- 对话历史清空和 Markdown 导出
- 检索 chunk 数量调节

## Structure

```text
03-financial-rag/
├── app.py                         # Streamlit Web 应用
├── data/                          # 本地 PDF 数据目录
├── reports/                       # 年报 / 研报目录
├── scripts/
│   ├── chunk_pdf.py               # PDF 文本切分实验脚本
│   ├── extract_pdf.py             # PDF 文本提取实验脚本
│   ├── index_chroma.py            # Chroma 建库实验脚本
│   ├── rag_engine.py              # RAG 核心流程
│   ├── rag_query.py               # RAG 查询实验脚本
│   └── rag_rerank.py              # 检索重排实验脚本
├── requirements.txt
└── .env.example
```

## Setup

```bash
cd 03-financial-rag
pip install -r requirements.txt
cp .env.example .env
```

把 `.env` 中的 `DEEPSEEK_API_KEY` 改成自己的 key。

## Run

```bash
streamlit run app.py
```

浏览器打开 `http://localhost:8501`。

## RAG Pipeline

```text
PDF
  -> pdfplumber 提取文本
  -> RecursiveCharacterTextSplitter 切分 chunk
  -> BAAI/bge-small-zh-v1.5 生成 embedding
  -> ChromaDB 持久化
  -> 用户提问
  -> 向量检索相关 chunk
  -> DeepSeek 基于上下文生成回答
  -> 展示回答和引用来源
```

## Core Files

| 文件 | 作用 |
|---|---|
| `app.py` | Streamlit 界面和交互逻辑 |
| `scripts/rag_engine.py` | 提取、切分、建库、检索、回答 |
| `requirements.txt` | 阶段 3 依赖 |
| `.env.example` | API key 配置示例 |

## Portfolio Value

这个项目是当前作品集的重点展示项目。它把金融 PDF、向量检索、LLM 生成和 Web UI 串成完整应用，比单次 API 调用更能体现 AI 金融工具开发能力。

## Data And Secrets

`.env`、`chroma_db/`、大体积 PDF 和运行生成文件不提交到 GitHub。示例配置只保留在 `.env.example`。
