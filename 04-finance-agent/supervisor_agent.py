from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["no_proxy"] = ".yahoo.com,.yimg.com,.eastmoney.com"
os.environ["NO_PROXY"] = ".yahoo.com,.yimg.com,.eastmoney.com"

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


# ========== State ==========
class AgentState(TypedDict):
    user_input: str
    history: List[str]
    stock_data: Optional[str]
    doc_data: Optional[str]
    final_report: Optional[str]
    next_worker: str


# ========== 模拟数据 ==========
STOCK_DB = {
    "600519": "贵州茅台 1523.50元 PE:25.3",
    "002594": "比亚迪 268.00元 PE:22.1",
}
DOC_DB = {
    "600519": "茅台2024年报：营收1500亿，净利润750亿",
    "002594": "比亚迪2024年报：营收6000亿，净利润300亿",
}


# ========== Supervisor（老板）==========
def supervisor_node(state: AgentState):
    """检查还缺什么数据，决定下一步"""
    history = state.get("history", [])

    if not state.get("stock_data"):
        history.append("Supervisor: 缺股票数据 → 调 stock_worker")
        return {"history": history, "next_worker": "stock_worker"}
    if not state.get("doc_data"):
        history.append("Supervisor: 缺文档数据 → 调 doc_worker")
        return {"history": history, "next_worker": "doc_worker"}
    if not state.get("final_report"):
        history.append("Supervisor: 数据齐全 → 调 report_worker 生成报告")
        return {"history": history, "next_worker": "report_worker"}
    history.append("Supervisor: 报告已生成 → 结束")
    return {"history": history, "next_worker": "finish"}


def supervisor_router(state: AgentState) -> str:
    return state.get("next_worker", "finish")


# ========== Workers ==========
def stock_worker(state: AgentState):
    symbol = "600519"
    if "比亚迪" in state["user_input"] or "002594" in state["user_input"]:
        symbol = "002594"
    data = STOCK_DB[symbol]
    history = state["history"] + [f"  Worker: 查 {symbol} 行情 → {data}"]
    return {"stock_data": data, "history": history}


def doc_worker(state: AgentState):
    symbol = "600519"
    if "比亚迪" in state["user_input"] or "002594" in state["user_input"]:
        symbol = "002594"
    data = DOC_DB.get(symbol, "未找到")
    history = state["history"] + [f"  Worker: 查 {symbol} 年报 → {data}"]
    return {"doc_data": data, "history": history}


def report_worker(state: AgentState):
    prompt = f"""基于以下数据，生成一份简洁的金融分析报告。

用户问题：{state['user_input']}

股票数据：{state.get('stock_data', '无')}
文档数据：{state.get('doc_data', '无')}
"""
    response = llm.invoke(prompt)
    history = state["history"] + ["  Worker: 报告已生成"]
    return {"final_report": response.content, "history": history}


# ========== 画图 ==========
workflow = StateGraph(AgentState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("stock_worker", stock_worker)
workflow.add_node("doc_worker", doc_worker)
workflow.add_node("report_worker", report_worker)

workflow.set_entry_point("supervisor")

workflow.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "stock_worker": "stock_worker",
        "doc_worker": "doc_worker",
        "report_worker": "report_worker",
        "finish": END,
    },
)

# Worker 干完活回到 Supervisor（让 Supervisor 检查下一步）
for worker in ["stock_worker", "doc_worker", "report_worker"]:
    workflow.add_edge(worker, "supervisor")

app = workflow.compile()


if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("你想查什么？")

    result = app.invoke(
        {
            "user_input": question,
            "history": [],
            "stock_data": None,
            "doc_data": None,
            "final_report": None,
            "next_worker": "",
        }
    )

    print("\n" + "=" * 40)
    print("执行记录：")
    for step in result["history"]:
        print(f"  {step}")
    print("\n最终报告：")
    print(result["final_report"])
