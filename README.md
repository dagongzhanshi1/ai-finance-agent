# 环境安装记录

## 安装日期
2026-05-03

## 已安装的软件

### 1. Miniconda (Python 环境管理)
- **路径:** `~/ai-conda/`
- **版本:** conda 26.3.2, Python 3.13
- **已安装的包（在 base 环境中）：**

#### 数据分析 & 金融数据
- pandas, numpy, matplotlib, seaborn
- jupyter, notebook
- yfinance（美股/A股数据）
- scikit-learn, xgboost

#### LLM & RAG
- openai（OpenAI API 客户端）
- python-dotenv（环境变量管理）
- pydantic（数据验证）
- langchain, langchain-community, langchain-openai
- langgraph（Agent 工作流）
- chromadb（向量数据库）
- faiss-cpu（向量检索）
- pdfplumber, pypdf（PDF 解析）

#### Web 界面
- streamlit

### 2. VS Code (代码编辑器)
- **路径:** `/Applications/Visual Studio Code.app`
- **CLI:** `/opt/homebrew/bin/code`
- **推荐插件（需要手动在 VS Code 中安装）:**
  - Python (ms-python.python)
  - Pylance (ms-python.vscode-pylance)
  - Jupyter (ms-toolsai.jupyter)
  - GitLens (eamodio.gitlens)
  - Error Lens (usernamehw.errorlens) ✅ 已装
  - GitHub Copilot (github.copilot)
- **配置文件:** `~/.vscode/` 已创建
- **项目 VS Code 配置:** `~/Projects/ai-finance-portfolio/.vscode/`

### 3. Git & GitHub
- **Git 版本:** 2.50.1 (系统自带)
- **SSH key 已生成:** `~/.ssh/id_ed25519.pub`
- **公钥：**
  ```
  ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIR3vQtubOuzNspgAzGb6RwXhiOIRgT+qG0P2Hz1Uy/B zmbgzx@github
  ```
- **配置步骤（下次手动操作）：**
  1. 打开 https://github.com/settings/ssh/new
  2. Title: "MacBook Air"
  3. Key: 粘贴上面的公钥
  4. 点击 Add SSH Key
  5. 回到终端运行：
     ```bash
     ssh -T git@github.com
     ```
     看到 "Hi xxx! You've successfully authenticated" 就成功了
  6. 然后推送代码：
     ```bash
     cd ~/Projects/ai-finance-portfolio
     git remote add origin git@github.com:zmbgzx/ai-finance-portfolio.git
     git push -u origin main
     ```

### 4. DBeaver (数据库管理工具)
- **路径:** `/Applications/DBeaver.app`
- **学习数据库文件:** `~/Projects/ai-finance-portfolio/01-stock-analysis/stock_learning.db`
- **使用方法:**
  1. 打开 DBeaver
  2. Database → New Database Connection → SQLite
  3. Browse → 选择 stock_learning.db
  4. Finish

### 5. Docker Desktop (后续部署用，暂未安装)
- 当前阶段用不到，第 10 周再装
- 安装命令：`brew install --cask docker`

---

## 项目目录结构

```
~/Projects/ai-finance-portfolio/
├── 01-stock-analysis/          # 阶段1：股票分析
│   ├── data/                   # 数据文件
│   ├── output/                 # 输出图片等
│   ├── sql/                    # SQL 学习文件
│   │   └── stock_learning.sql
│   └── stock_learning.db       # SQLite 练习数据库
├── .vscode/                    # VS Code 配置
│   ├── extensions.json
│   └── settings.json
├── Miniconda3-latest-MacOSX-arm64.sh  # 安装脚本（可删除）
├── verify_setup.py             # 环境验证脚本
├── README.md                   # 仓库说明
└── .gitignore
```

## 日常使用

每次打开终端后，需要先激活 conda 环境：
```bash
export PATH="$HOME/ai-conda/bin:$PATH"
# 或加到 ~/.bash_profile 中自动生效：
# echo 'export PATH="$HOME/ai-conda/bin:$PATH"' >> ~/.bash_profile
```

## 下一步

按照 [[01-阶段1-Python与数据分析]] 从 Day 1 开始学习。
