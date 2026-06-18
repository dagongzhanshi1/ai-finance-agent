import streamlit as st

st.set_page_config(page_title="金融研报问答", layout="wide")
st.title("金融文档 RAG 问答系统")

from scripts.rag_engine import rag_query, build_index
from pathlib import Path
import os
import tempfile
import chromadb


# 从 Chroma 数据库读取已存在的集合
def get_collections():
    client = chromadb.PersistentClient(path="./chroma_db")
    collections = client.list_collections()
    names = [c.name for c in collections]
    return names if names else ["maotai_2025"]


def get_collection_info(collection_name):
    """获取集合中的 chunk 数量"""
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(name=collection_name)
        return collection.count()
    except Exception:
        return 0


# 侧边栏
st.sidebar.header("文档库")
uploaded_file = st.sidebar.file_uploader("上传 PDF 年报", type=["pdf"])

# 防止同一文件重复建库
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

collection_name = st.sidebar.selectbox(
    "选择文档库",
    get_collections(),
)

# 显示当前库信息
chunk_count = get_collection_info(collection_name)
st.sidebar.caption(f"当前库: {collection_name}")
st.sidebar.caption(f"chunk 数量: {chunk_count}")

st.sidebar.divider()
st.sidebar.header("检索参数")
top_k = st.sidebar.slider("检索 chunk 数量 (k)", min_value=1, max_value=20, value=5)

if uploaded_file is not None:
    import re
    base_name = uploaded_file.name.replace(".pdf", "").replace(" ", "_")
    safe_name = re.sub(r"[^a-zA-Z0-9._-]", "", base_name)
    collection_name = f"custom_{safe_name}"

    if uploaded_file.name not in st.session_state.processed_files:
        st.session_state.processed_files.add(uploaded_file.name)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner(f"正在索引: {uploaded_file.name}..."):
            build_index(temp_path, collection_name=collection_name)
        st.sidebar.success(f"已建库: {collection_name}")

# 主区域 - 标签页
tab1, tab2 = st.tabs(["查询", "文档管理"])

with tab1:
    # 初始化聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.markdown(f"**当前文档: {collection_name}**")

    # 显示聊天历史
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 输入框
    question = st.chat_input("请输入你的问题：")

    if question:
        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("正在查询..."):
            answer, chunks = rag_query(question, collection_name=collection_name, k=top_k)

        with st.chat_message("assistant"):
            st.markdown(answer)
            with st.expander("查看引用来源"):
                for i, chunk in enumerate(chunks, 1):
                    st.markdown(f"**来源 {i}**")
                    st.text(chunk[:300])

        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": answer})

    # 清空和导出按钮
    if st.session_state.messages:
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.button("清空对话历史", on_click=lambda: st.session_state.messages.clear())
        with col_b:
            md_text = f"# 金融研报问答记录\n\n"
            for msg in st.session_state.messages:
                role = "你" if msg["role"] == "user" else "助手"
                md_text += f"**{role}：**\n\n{msg['content']}\n\n---\n\n"
            st.download_button(
                "导出为 Markdown",
                data=md_text,
                file_name="rag_对话记录.md",
                mime="text/markdown",
            )

with tab2:
    st.markdown("**已有文档库**")

    # 初始化确认删除状态
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = None

    for name in get_collections():
        count = get_collection_info(name)
        col1, col2, col3 = st.columns([4, 2, 2])

        with col1:
            st.markdown(f"{name}（{count} 个 chunk）")

        with col2:
            rename_key = f"rename_{name}"
            new_name = st.text_input("新名称", key=rename_key, label_visibility="collapsed")
            if new_name and st.button("重命名", key=f"btn_{name}"):
                import re
                if not re.match(r"^[a-zA-Z0-9._-]+$", new_name):
                    st.error("名称只能包含英文、数字、点、下划线、短横线")
                elif new_name == name:
                    st.warning("新名称与原名相同")
                else:
                    client = chromadb.PersistentClient(path="./chroma_db")
                    old_col = client.get_collection(name=name)
                    all_data = old_col.get(include=["embeddings", "documents"])
                    new_col = client.create_collection(name=new_name)
                    new_col.add(
                        embeddings=all_data["embeddings"],
                        documents=all_data["documents"],
                        ids=all_data["ids"],
                    )
                    client.delete_collection(name=name)
                    st.rerun()

        with col3:
            if st.button("删除", key=f"del_{name}"):
                if st.session_state.confirm_delete == name:
                    client = chromadb.PersistentClient(path="./chroma_db")
                    client.delete_collection(name=name)
                    st.session_state.confirm_delete = None
                    st.rerun()
                else:
                    st.session_state.confirm_delete = name
                    st.rerun()

        # 显示确认提示
        if st.session_state.confirm_delete == name:
            st.warning(f"再次点击「删除」确认删除 {name}")
