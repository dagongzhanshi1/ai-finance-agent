import logging
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["no_proxy"] = ".yahoo.com,.yimg.com,.eastmoney.com"
os.environ["NO_PROXY"] = ".yahoo.com,.yimg.com,.eastmoney.com"

# ========== 日志设置 ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),   # 同时写入文件
        logging.StreamHandler()              # 同时打印到终端
    ]
)
logger = logging.getLogger(__name__)
# ==============================

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


class AgentState(TypedDict):
    symbol: str
    stock_info: Optional[str]
    financial_info: Optional[str]
    news: Optional[str]
    report: Optional[str]


def search_stock(state: AgentState):
    logger.info(f"开始查 {state['symbol']} 实时行情")
    if state["symbol"] == "600519":
        data = "贵州茅台（600519）\n最新价: 1523.50元  涨跌幅: +1.2%\n市盈率: 25.3"
        logger.info(f"查到数据：1523.50元")
        return {"stock_info": data}
    elif state["symbol"] == "002594":
        data = "比亚迪（002594）\n最新价: 268.00元  涨跌幅: -0.8%\n市盈率: 22.1"
        logger.info(f"查到数据：268.00元")
        return {"stock_info": data}
    else:
        logger.warning(f"未找到 {state['symbol']} 的数据")
        return {"stock_info": "没有找到"}


def search_financial(state: AgentState):
    logger.info(f"开始查 {state['symbol']} 财务数据")
    if state["symbol"] == "600519":
        return {"financial_info": "营收: 1500.00亿\n净利润: 750.00亿\n毛利率: 93.5%"}
    elif state["symbol"] == "002594":
        return {"financial_info": "营收: 6000.00亿\n净利润: 300.00亿\n毛利率: 20.1%"}
    else:
        return {"financial_info": "未知"}


def search_news_node(state: AgentState):
    logger.info(f"开始搜 {state['symbol']} 新闻")
    if state["symbol"] == "600519":
        return {"news": "贵州茅台 最新新闻：\n1. [财联社] 茅台2024年营收同比增长15%\n2. [证券时报] 北向资金增持茅台"}
    elif state["symbol"] == "002594":
        return {"news": "比亚迪 最新新闻：\n1. [36氪] 比亚迪海外市场销量创新高\n2. [第一财经] 比亚迪新一代电池技术发布"}
    else:
        return {"news": "暂无相关新闻"}


def generate_report(state: AgentState):
    logger.info("调用 LLM 生成分析报告")
    prompt = f"""你是一个金融分析师。基于以下数据，生成一份简洁的个股分析报告。

股票代码：{state['symbol']}

【实时行情】
{state['stock_info']}

【财务指标】
{state['financial_info']}

【最新新闻】
{state['news']}

请包含：
1. 公司基本情况
2. 估值分析（PE 是否合理）
3. 近期财务表现
4. 新闻要点
5. 一句话总结
"""
    response = llm.invoke(prompt)
    logger.info(f"LLM 返回 {len(response.content)} 字")
    return {"report": response.content}


def no_data(state: AgentState):
    logger.error(f"{state['symbol']} 所有数据源均无数据")
    return {"report": f"❌ 无法获取 {state['symbol']} 的数据，请检查股票代码是否正确。"}


def check_stock_data(state: AgentState) -> str:
    if "没有找到" in (state.get("stock_info") or ""):
        logger.warning("数据为空，跳转到错误处理")
        return "no_data"
    logger.info("数据正常，继续后续查询")
    return "continue"


workflow = StateGraph(AgentState)

workflow.add_node("search_stock", search_stock)
workflow.add_node("search_financial", search_financial)
workflow.add_node("search_news", search_news_node)
workflow.add_node("generate_report", generate_report)
workflow.add_node("no_data", no_data)

workflow.set_entry_point("search_stock")

workflow.add_conditional_edges(
    "search_stock",
    check_stock_data,
    {
        "continue": "search_financial",
        "no_data": "no_data",
    }
)

workflow.add_edge("search_financial", "search_news")
workflow.add_edge("search_news", "generate_report")
workflow.add_edge("generate_report", END)
workflow.add_edge("no_data", END)

app = workflow.compile()
