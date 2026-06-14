# 金融新闻摘要工具 📰

输入一段金融新闻文本 → 自动生成结构化摘要（JSON）。

## 功能

- 调用 DeepSeek API 分析金融新闻
- 输出结构化 JSON：标题、摘要、关键要点、情绪、相关公司
- 三种输入模式：文件 / 管道 / 交互
- 结果自动保存为 JSON 文件

## 用法

```bash
# 交互模式：直接运行，粘贴新闻文本
python3 main.py

# 文件模式：传入文本文件
python3 main.py 新闻.txt

# 管道模式：从其他命令输入
cat 新闻.txt | python3 main.py
```

## 项目结构

```
02-news-summarizer/
  ├── config.py       # API 配置
  ├── summarizer.py   # 核心逻辑：Pydantic 模型 + API 调用
  ├── main.py         # CLI 入口
  ├── utils.py        # 格式化输出 + JSON 保存
  ├── .env            # API key
  └── .gitignore
```

## 依赖

```bash
pip install openai python-dotenv pydantic
```

## 技术栈

- Python + DeepSeek API
- Pydantic（数据校验）
- JSON（结构化输出）
