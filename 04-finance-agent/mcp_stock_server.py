"""
mcp_stock_server.py — MCP 股票查询服务器
通过 stdio 协议暴露股票查询工具，任何 MCP 客户端（Hermes、Claude Code 等）都能连接使用。

运行方式：
  python mcp_stock_server.py

配置到 Hermes（~/.hermes/config.yaml）：
  mcp_servers:
    stock:
      command: "python"
      args: ["/path/to/04-finance-agent/mcp_stock_server.py"]
"""
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import yfinance as yf

# ========== 工具实现 ==========
STOCK_DATA = {
    "600519": {"name": "贵州茅台", "price": "1523.50", "pe": "25.3", "change": "+1.2%"},
    "002594": {"name": "比亚迪", "price": "268.00", "pe": "22.1", "change": "-0.8%"},
}


async def get_stock_price(symbol: str) -> str:
    """查询 A 股实时股价"""
    if symbol in STOCK_DATA:
        s = STOCK_DATA[symbol]
        return f"{s['name']} 当前股价: {s['price']}元  涨跌幅: {s['change']}"
    return f"未找到股票 {symbol}"


async def get_company_info(symbol: str) -> str:
    """查询公司基本信息"""
    if symbol in STOCK_DATA:
        s = STOCK_DATA[symbol]
        pe = s["pe"]
        return f"{s['name']}（{symbol}）\n最新价: {s['price']}元\n市盈率: {pe}"
    return f"未找到股票 {symbol}"


# ========== 创建 MCP 服务器 ==========
server = Server("stock-server")


@server.list_tools()
async def handle_list_tools():
    """告诉客户端：我有哪些工具"""
    from mcp.types import Tool, TextContent

    return [
        Tool(
            name="get_stock_price",
            description="查询A股实时股价",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码，如 600519（茅台）或 002594（比亚迪）",
                    }
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_company_info",
            description="查询公司基本信息（行业、市值）",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码",
                    }
                },
                "required": ["symbol"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    """客户端调工具时执行这里"""
    from mcp.types import TextContent

    if name == "get_stock_price":
        result = await get_stock_price(arguments["symbol"])
    elif name == "get_company_info":
        result = await get_company_info(arguments["symbol"])
    else:
        result = f"未知工具: {name}"

    return [TextContent(type="text", text=result)]


# ========== 启动 ==========
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="stock-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
