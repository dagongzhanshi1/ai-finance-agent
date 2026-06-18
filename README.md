# AI 金融求职 — 学习项目

Python + LLM 驱动的金融分析学习项目。从股票分析到 AI Agent，一步步搭建金融研究工具集。

## 项目结构

```
ai-finance-portfolio/
├── 01-stock-analysis/         # 阶段1：Python + 数据分析
│   ├── 01-basic.py            # Day 1-2：Python 基础
│   ├── 02-pandas-intro.py     # Day 3：Pandas 入门
│   ├── 03-plot.py             # Day 4：Matplotlib 画图
│   ├── 05-preview-groupby-merge.py  # Day 7：分组与合并
│   ├── 06-day8-groupby-merge.py     # Day 8：进阶分组
│   ├── 07-day8-exercises.py         # Day 8：练习题
│   ├── 08-day9-download.py          # Day 9：yfinance 数据下载
│   ├── 09-day10-analyze.py          # Day 10：风险收益指标计算
│   ├── 10-day11-visualize.py        # Day 11：净值曲线 + 热力图
│   ├── 11-semiconductor-analysis.py # 半导体行业扩展分析
│   ├── sql/                    # SQL 学习
│   │   ├── 04-sqlite-python.py
│   │   ├── stock_learning.sql
│   │   ├── day6_practice.sql
│   │   └── stock_learning.db
│   ├── data/                   # 数据文件
│   └── output/                 # 输出图表
│       ├── nav_curve.png
│       ├── correlation_heatmap.png
│       ├── semiconductor_nav.png
│       └── semiconductor_heatmap.png
│
├── 02-news-summarizer/        # 阶段2：LLM + Prompt Engineering
│   ├── 01-first-call.py              # Day 15：首次调用 DeepSeek API
│   ├── 02-prompt-lab.py              # Day 16：结构化 Prompt 实验
│   ├── 03-structured-output.py       # Day 17：JSON 强制输出 + Pydantic
│   ├── 03-structured-output-practice.py  # Day 17：练习 — 股票推荐模型
│   └── 04-function-calling.py        # Day 18：Function Calling 三步走
│
├── 03-financial-rag/          # 阶段3：RAG 知识库 + Streamlit
│   ├── app.py                       # Streamlit Web 界面
│   ├── scripts/
│   │   └── rag_engine.py            # RAG 引擎（5 个核心函数）
│   ├── .env                         # API 密钥（需自行配置）
│   ├── requirements.txt             # 本模块依赖
│   └── .gitignore                   # 忽略 chroma_db/ data/ .env
│
├── .gitignore
├── README.md
├── requirements.txt
└── verify_setup.py
```

## 阶段 1：Python + 数据分析（Day 1-12）

分析 A 股多只股票的历史数据，计算风险收益指标。

### 功能

- 用 yfinance 下载多只股票历史数据
- 计算年化收益率、年化波动率、最大回撤、夏普比率
- 画累计净值曲线对比图（标注最大回撤位置）
- 画股票日收益率相关性热力图
- SQLite 数据库操作练习

### 使用方式

```bash
# 安装依赖
pip install -r requirements.txt

# 下载数据
python 01-stock-analysis/08-day9-download.py

# 分析（计算风险收益指标）
python 01-stock-analysis/09-day10-analyze.py

# 可视化
python 01-stock-analysis/10-day11-visualize.py
```

### 分析结果示例

| 股票 | 年化收益率 | 年化波动率 | 最大回撤 | 夏普比率 |
|------|-----------|-----------|---------|---------|
| 茅台 | 15.2% | 22.1% | -18.5% | 0.68 |
| 宁德时代 | 248.12% | — | — | — |

（注：具体数值随下载时间段变化。）

## 阶段 2：LLM API + Prompt Engineering（Day 15-18）

用 DeepSeek API（兼容 OpenAI 格式）构建金融新闻摘要工具的基础能力。

### 学习路线

| Day | 主题 | 代码 |
|-----|------|------|
| 15 | 首次 API 调用 | `01-first-call.py` |
| 16 | 结构化 Prompt 实验 | `02-prompt-lab.py` |
| 17 | Structured Output（JSON + Pydantic） | `03-structured-output.py` |
| 17 练习 | 自己写 StockRecommendation 模型 | `03-structured-output-practice.py` |
| 18 | Function Calling（工具定义 + 三步走） | `04-function-calling.py` |

### 核心概念

- **Structured Output**：让 LLM 返回 JSON 格式数据，而不是自然语言
- **Pydantic BaseModel**：用 Python class 定义数据结构，自动做类型校验
- **Function Calling**：模型选择工具 → 代码执行 → 结果回传 → 模型回答
- **Tool Schema**：用 JSON Schema 描述函数名、参数、用途

### 使用方式

```bash
# 先配 API key（用 DeepSeek）
cd 02-news-summarizer
cp .env.example .env   # 填入你的 DEEPSEEK_API_KEY

# 跑 Day 18 Function Calling
python 04-function-calling.py
```

## 阶段 3：RAG 知识库 + Streamlit Web 界面（Day 29-35）

基于 RAG（Retrieval-Augmented Generation）的金融文档问答系统。上传 PDF 年报，用自然语言提问，LLM 基于检索到的原文回答。

### 功能

- 上传 PDF 年报 → 自动切分 → Embedding → 存入 Chroma 向量数据库
- 自然语言提问，检索最相关的段落 + LLM 生成回答
- Cross-Encoder Rerank 提升检索精度
- 引用来源展示，方便核实验证
- 聊天式对话历史，可导出 Markdown
- 文档库管理：选择、重命名、删除

### 技术栈

| 组件 | 技术 |
|------|------|
| 前端 | Streamlit |
| 文本提取 | pdfplumber |
| 文本切分 | RecursiveCharacterTextSplitter（LangChain） |
| Embedding 模型 | BAAI/bge-small-zh-v1.5（本地 512 维） |
| 向量数据库 | ChromaDB（本地持久化） |
| Rerank 模型 | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| 生成模型 | DeepSeek-v4-Flash（OpenAI 兼容 API） |

### 使用方式

```bash
cd 03-financial-rag

# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API 密钥（.env 文件）
echo "DEEPSEEK_API_KEY=你的密钥" > .env

# 3. 放一份年报 PDF 到 data/ 目录

# 4. 启动 Web 界面
streamlit run app.py

# 浏览器打开 http://localhost:8501
# 侧边栏可上传多份 PDF 并切换文档库
```

### RAG 流程

```text
PDF → pdfplumber 提取文本 → RecursiveCharacterTextSplitter 切分（500+100）
    → bge-small-zh Embedding（512 维）
    → ChromaDB 存储
    → 用户提问 → Embedding 检索 20 个 → Cross-Encoder Rerank → top 5
    → DeepSeek 生成回答 → 带引用来源展示
```

### 查询结果示例

```
问：宁德时代 2025 年的毛利率和净利率是多少？
答：毛利率约为 26.27%（营收 4,237 亿，成本 3,123 亿），
    净利率约为 17.04%（净利润 722 亿）。
    （引用来源：年报"营业收入和营业成本"及"净利润"片段）
```

## 数据来源

- Yahoo Finance（通过 yfinance 库获取）
- DeepSeek API（OpenAI 兼容格式）

## 环境要求

- Python 3.10+
- 依赖包见 requirements.txt
- DeepSeek API key（或兼容 OpenAI 格式的其他 API）
