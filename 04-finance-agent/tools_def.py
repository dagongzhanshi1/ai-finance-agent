"""tools_def.py - 共享工具定义，agent_langchain.py 和 app.py 都从这里导入"""
import os
import sys

# ========== 代理设置 ==========
EASTMONEY_NO_PROXY_HOSTS = [
    "82.push2.eastmoney.com",
    "push2.eastmoney.com",
    ".eastmoney.com",
    "*.eastmoney.com",
]


def add_no_proxy_hosts(hosts: list[str]) -> None:
    for key in ("no_proxy", "NO_PROXY"):
        current = [item.strip() for item in os.getenv(key, "").split(",") if item.strip()]
        merged = current + [host for host in hosts if host not in current]
        os.environ[key] = ",".join(merged)


add_no_proxy_hosts(EASTMONEY_NO_PROXY_HOSTS)

from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()


# ========== 工具定义 ==========

@tool
def get_stock_price(symbol: str) -> str:
    """查询 A 股实时股价，输入股票代码（如 600519.SS=上交所茅台）"""
    import yfinance as yf
    stock = yf.Ticker(symbol)
    info = stock.info
    price = info.get("currentPrice")
    name = info.get("longName")
    return f"{name} 当前股价: {price} 元"


@tool
def get_pe_ratio(symbol: str) -> str:
    """查询股票市盈率(PE)，输入股票代码"""
    import yfinance as yf
    stock = yf.Ticker(symbol)
    info = stock.info
    pe = info.get("trailingPE")
    name = info.get("longName")
    return f"{name} 市盈率(PE): {pe}"


@tool
def get_stock_change(symbol: str) -> str:
    """查询股票今日涨跌幅百分比，输入股票代码"""
    import yfinance as yf
    stock = yf.Ticker(symbol)
    info = stock.info
    price = info.get("currentPrice")
    change_pct = info.get("regularMarketChangePercent")
    name = info.get("longName")
    return f"{name} 当前价: {price}元  涨跌幅: {change_pct:.2f}%"


@tool
def get_company_info(symbol: str) -> str:
    """查询公司基本信息（行业、市值），输入股票代码"""
    import yfinance as yf
    stock = yf.Ticker(symbol)
    info = stock.info
    name = info.get("longName")
    sector = info.get("sector")
    industry = info.get("industry")
    market_cap = info.get("marketCap")
    if market_cap:
        market_cap = f"{market_cap / 100000000:.0f}亿"
    return f"{name}\n行业: {sector} - {industry}\n市值: {market_cap}"


@tool
def get_volume(symbol: str) -> str:
    """查询股票今日成交量（股数），输入股票代码"""
    import yfinance as yf
    stock = yf.Ticker(symbol)
    info = stock.info
    volume = info.get("volume")
    name = info.get("longName")
    return f"{name} 今日成交量: {volume} 股"


@tool
def get_52week_range(symbol: str) -> str:
    """查询股票52周（一年）内的最高价和最低价，输入股票代码"""
    import yfinance as yf
    stock = yf.Ticker(symbol)
    info = stock.info
    high = info.get("fiftyTwoWeekHigh")
    low = info.get("fiftyTwoWeekLow")
    name = info.get("longName")
    return f"{name} 52周范围: 最低{low}元 - 最高{high}元"


@tool
def get_financial_metrics(symbol: str) -> str:
    """查询公司的财务指标（营收、净利润、毛利率），输入股票代码"""
    import yfinance as yf
    stock = yf.Ticker(symbol)
    info = stock.info
    name = info.get("longName", symbol)
    revenue = info.get("totalRevenue")
    net_income = info.get("netIncomeToCommon")
    gross_margin = info.get("grossMargins")
    revenue_str = f"{revenue / 1e8:.2f}亿" if revenue else "未知"
    income_str = f"{net_income / 1e8:.2f}亿" if net_income else "未知"
    margin_str = f"{gross_margin * 100:.1f}%" if gross_margin else "未知"
    return f"{name}\n营收: {revenue_str}\n净利润: {income_str}\n毛利率: {margin_str}"


@tool
def search_news(symbol: str) -> str:
    """查询股票最新相关新闻（最多5条），输入股票代码"""
    import yfinance as yf
    stock = yf.Ticker(symbol)
    news = stock.news
    name = stock.info.get("longName", symbol)
    if not news:
        return f"{name} 暂无相关新闻"
    result = [f"{name} 最新新闻："]
    for i, article in enumerate(news[:5], 1):
        content = article.get("content", {})
        title = content.get("title", "无标题")
        provider = content.get("provider", {}).get("displayName", "")
        date = content.get("pubDate", "")[:10]
        result.append(f"{i}. [{provider}] {title}（{date}）")
    return "\n".join(result)


@tool
def get_ashare_price(symbol: str) -> str:
    """查询A股实时行情（东方财富数据源），输入6位股票代码（如600519=茅台）。比get_stock_price更快更稳定，推荐用于A股"""
    import akshare as ak
    try:
        df = ak.stock_zh_a_spot_em()
    except Exception:
        import yfinance as yf
        suffix = ".SS" if symbol.startswith("6") else ".SZ"
        stock = yf.Ticker(symbol + suffix)
        info = stock.info
        name = info.get("longName", symbol)
        price = info.get("currentPrice", "未知")
        change = info.get("regularMarketChangePercent")
        change_str = f"{change:.2f}%" if change else "未知"
        return f"{name}（{symbol}）\n最新价: {price}元  涨跌幅: {change_str}%\n数据来源: Yahoo Finance"
    row = df[df["代码"] == symbol]
    if row.empty:
        return f"未找到代码 {symbol}"
    r = row.iloc[0]
    return f"{r['名称']}（{symbol}）\n最新价: {r['最新价']}元  涨跌幅: {r['涨跌幅']}%\n今开: {r['今开']}  昨收: {r['昨收']}\n最高: {r['最高']}  最低: {r['最低']}\n市盈率: {r['市盈率-动态']}  总市值: {r['总市值']}亿\n数据来源: 东方财富"


@tool
def get_ashare_pe(symbol: str) -> str:
    """查询A股动态市盈率（东方财富数据源），输入6位股票代码"""
    import akshare as ak
    try:
        df = ak.stock_zh_a_spot_em()
    except Exception:
        import yfinance as yf
        suffix = ".SS" if symbol.startswith("6") else ".SZ"
        stock = yf.Ticker(symbol + suffix)
        pe = stock.info.get("trailingPE", "未知")
        name = stock.info.get("longName", symbol)
        return f"{name}（{symbol}）动态市盈率: {pe}"
    row = df[df['代码'] == symbol]
    if row.empty:
        return f"未找到代码 {symbol}"
    r = row.iloc[0]
    return f"{r['名称']}（{symbol}）动态市盈率: {r['市盈率-动态']}"


@tool
def query_financial_docs(question: str, collection_name: str = "maotai") -> str:
    """查询已上传的金融文档知识库（年报/研报），输入你的问题。不记得有哪些文档库时先用 list_doc_collections 查看可用库名"""
    phase3_path = os.path.join(os.path.dirname(__file__), "..", "03-financial-rag")
    if phase3_path not in sys.path:
        sys.path.insert(0, phase3_path)
    from scripts.rag_engine import rag_query
    chroma_path = os.path.join(phase3_path, "chroma_db")
    answer, chunks = rag_query(question, collection_name=collection_name, chroma_path=chroma_path, k=5)
    return f"回答：{answer}\n\n（基于 {collection_name} 知识库，参考了 {len(chunks)} 个文档片段）"


@tool
def list_doc_collections() -> str:
    """列出金融文档知识库里所有可用的文档集合名称，查询文档前先用这个看有哪些库"""
    import chromadb
    phase3_path = os.path.join(os.path.dirname(__file__), "..", "03-financial-rag")
    chroma_path = os.path.join(phase3_path, "chroma_db")
    client = chromadb.PersistentClient(path=chroma_path)
    cols = client.list_collections()
    if not cols:
        return "当前没有可用的文档库。"
    return f"可用文档库：\n" + "\n".join(f"- {c.name}" for c in cols)


# ========== 按分类分组的工具列表（用于 Streamlit 侧边栏） ==========
ALL_TOOLS_GROUPS = {
    "实时行情-东方财富": [get_ashare_price, get_ashare_pe],
    "实时行情-Yahoo": [get_stock_price, get_pe_ratio, get_stock_change, get_company_info, get_volume, get_52week_range],
    "财务指标": [get_financial_metrics],
    "新闻": [search_news],
    "RAG文档库": [query_financial_docs, list_doc_collections],
}

# 所有工具的平铺列表
ALL_TOOLS = sum(ALL_TOOLS_GROUPS.values(), [])
