# 04-finance-agent 快捷命令
# 用法：make <命令>

help:           ## 显示所有命令
	@grep -E '^[a-zA-Z_-]+:.*##' Makefile | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ========== 测试 ==========

test:           ## 测试所有路径（成功 + 错误）
	python cli.py 600519
	@echo ""
	python cli.py 000000

# ========== 运行 ==========

run:            ## 命令行查询（例：make run s=002594）
	python cli.py $(s)

streamlit:      ## 启动 Streamlit Web 界面
	streamlit run app.py --server.port 8501

supervisor:     ## 启动 Supervisor Agent（例：make supervisor q="查一下茅台"）
	python supervisor_agent.py $(q)

mcp:            ## 启动 MCP 服务器
	python mcp_stock_server.py

# ========== 清理 ==========

clean:          ## 删除日志和缓存
	rm -f agent.log
	rm -rf __pycache__ .pytest_cache
	find . -name "*.pyc" -delete
