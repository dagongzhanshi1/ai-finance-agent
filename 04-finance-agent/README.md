# AI Finance Agent — 阶段 4

基于 LangGraph 的多步金融分析 Agent，支持固定工作流、Supervisor 模式和 MCP 协议扩展。

## 项目结构

```text
04-finance-agent/
├── workflow.py             # LangGraph 工作流（查行情→查财务→搜新闻→LLM报告）
├── cli.py                  # 命令行入口
├── app.py                  # Streamlit Web 界面
├── tools_def.py            # @tool 工具定义（含东方财富/RAG 工具）
├── agent_langchain.py      # LangChain create_agent 版 Agent
├── supervisor_agent.py     # Supervisor Agent 模式
├── mcp_stock_server.py     # MCP 股票查询服务器
├── README.md
└── .gitignore
```

## 使用方式

### 命令行查询

```bash
python cli.py 600519         # 查茅台
python cli.py 002594         # 查比亚迪
```

### Streamlit Web 界面

```bash
streamlit run app.py
```

### Supervisor Agent 模式

```bash
python supervisor_agent.py 查一下茅台
python supervisor_agent.py 分析比亚迪的股价和年报
```

### MCP 服务器（供外部客户端连接）

```bash
python mcp_stock_server.py
```

然后在 Hermes config.yaml 中配置：

```yaml
mcp_servers:
  stock:
    command: "/path/to/python"
    args: ["/path/to/mcp_stock_server.py"]
```

## 工作流结构

```text
search_stock → 查到 → search_financial → search_news → generate_report → END
                ↓
              查不到 → no_data → END
```

各节点通过 State（字典）传递数据，最终由 LLM 生成分析报告。

## Supervisor 模式

```text
Supervisor（检查 State，决定下一步）
  → stock_worker / doc_worker / report_worker
  → 回到 Supervisor 再检查
  → ...直到 finish → END
```

## 技术栈

- **LangGraph** — 有状态工作流引擎
- **LangChain** — LLM 调用封装 + @tool
- **DeepSeek API** — AI 模型
- **MCP** — 工具协议（Hermes 原生支持）
- **Streamlit** — Web 界面
