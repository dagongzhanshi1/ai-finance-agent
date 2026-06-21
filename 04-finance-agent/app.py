"""app.py - Streamlit Web 界面版金融 Agent"""
import os
import sys
import io
import contextlib
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools_def import ALL_TOOLS_GROUPS, ALL_TOOLS

load_dotenv()


# ========== 工具函数 ==========
def run_agent(prompt, active_tools, llm):
    """执行 agent，捕获 stdout/stderr 返回调试信息"""
    f = io.StringIO()
    agent = create_agent(
        model=llm,
        tools=active_tools,
        system_prompt="你是一个金融数据助手。根据用户的问题调用对应的工具来获取数据，然后用数据回答用户。",
    )
    with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
        result = agent.invoke({"messages": [("user", prompt)]})
    return result["messages"][-1].content, f.getvalue()


# ========== Streamlit 界面 ==========
st.set_page_config(page_title="AI 金融助手 Agent", page_icon="📈", layout="wide")

with st.sidebar:
    st.title("🤖 金融助手")
    st.markdown("---")

    st.subheader("🔧 启用工具")
    enabled_groups = {}
    for group_name in ALL_TOOLS_GROUPS:
        enabled_groups[group_name] = st.checkbox(group_name, value=True)

    active_tools = []
    for group_name, tools_list in ALL_TOOLS_GROUPS.items():
        if enabled_groups.get(group_name, True):
            active_tools.extend(tools_list)

    st.markdown("---")
    st.subheader("⚙️ 模型参数")
    temperature = st.slider("Temperature", 0.0, 1.5, 0.0, 0.1)
    show_debug = st.checkbox("显示思考过程 (debug)", value=False)

    st.markdown("---")
    st.caption("数据来源：东方财富 / Yahoo Finance / RAG 知识库")
    st.caption(f"已启用 {len(active_tools)} 个工具")

    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("📈 AI 金融助手")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("输入你的问题，例如「茅台今天股价多少？」"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
        temperature=temperature,
    )

    with st.chat_message("assistant"):
        with st.spinner("查询中..."):
            try:
                reply, debug_output = run_agent(prompt, active_tools, llm)
                if show_debug and debug_output.strip():
                    with st.expander("🔍 思考过程", expanded=False):
                        st.text(debug_output)
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                error_msg = f"❌ 查询失败: {type(e).__name__}: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
