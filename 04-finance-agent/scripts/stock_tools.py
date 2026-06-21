import yfinance as yf


def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    price = info.get("currentPrice")
    name = info.get("longName")
    return f"{name} 当前股价: {price} 元"


def get_pe_ratio(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    pe = info.get("trailingPE")
    name = info.get("longName")
    return f"{name} 市盈率(PE): {pe}"


def get_company_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    name = info.get("longName")
    sector = info.get("sector")
    industry = info.get("industry")
    market_cap = info.get("marketCap")
    if market_cap:
        market_cap = f"{market_cap / 100000000:.0f}亿"
    return f"{name}\n行业: {sector} - {industry}\n市值: {market_cap}"


def get_stock_change(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    price = info.get("currentPrice")
    change_pct = info.get("regularMarketChangePercent")
    name = info.get("longName")
    return f"{name} 当前价: {price}元  涨跌幅: {change_pct:.2f}%"


def get_volume(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    volume = info.get("volume")
    name = info.get("longName")
    return f"{name} 今日成交量: {volume} 股"


def get_52week_range(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info
    high = info.get("fiftyTwoWeekHigh")
    low = info.get("fiftyTwoWeekLow")
    name = info.get("longName")
    return f"{name} 52周范围: 最低{low}元 - 最高{high}元"


def get_financial_metrics(symbol):
    """查询公司的财务指标：营收、利润、毛利率"""
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


def search_news(symbol):
    """查询股票最新相关新闻"""
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
