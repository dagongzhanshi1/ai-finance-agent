import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb


def load_document(pdf_path):
    """从任意 PDF 文件提取文本"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n--- 分页 ---\n"
    return text


def split_document(text, chunk_size=500, chunk_overlap=100):
    """将文本切分成 chunk"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
    )
    return splitter.split_text(text)


def build_index(pdf_path, collection_name, chroma_path="./chroma_db"):
    """完整建库：提取 → 切分 → Embedding → 存入 Chroma"""
    print(f"正在提取: {pdf_path}")
    text = load_document(pdf_path)
    print(f"提取完成，总字符数: {len(text)}")

    print("正在切分 chunk...")
    chunks = split_document(text)
    print(f"切分成 {len(chunks)} 个 chunk")

    print("加载 Embedding 模型...")
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5", local_files_only=True)

    print("正在生成 Embedding...")
    embeddings = model.encode(chunks, show_progress_bar=True)

    print(f"连接 Chroma（{chroma_path}）...")
    chroma_client = chromadb.PersistentClient(path=chroma_path)
    collection = chroma_client.get_or_create_collection(name=collection_name)

    # 清空旧数据（仅在已有数据时）
    existing_ids = collection.get()["ids"]
    if existing_ids:
        collection.delete(ids=existing_ids)

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(
        embeddings=embeddings.tolist(),
        documents=chunks,
        ids=ids,
    )

    print(f"已存入 {collection.count()} 个 chunk")
    return collection_name, chroma_path


def search(query, collection_name, chroma_path="./chroma_db", k=5):
    """从 Chroma 检索最相关的 k 个 chunk"""
    # 连接 Chroma
    chroma_client = chromadb.PersistentClient(path=chroma_path)
    collection = chroma_client.get_collection(name=collection_name)

    # Embedding 模型（本地模式，不访问网络）
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5", local_files_only=True)

    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
    )
    return results["documents"][0]


def rag_query(question, collection_name, chroma_path="./chroma_db", k=5):
    """RAG 问答：检索 + LLM 回答"""
    load_dotenv()
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    API_BASE_URL = "https://api.deepseek.com/v1"
    MODEL_NAME = "deepseek-v4-flash"

    # 检索
    chunks = search(question, collection_name, chroma_path, k)
    context = "\n\n---\n\n".join(chunks)

    # 构造 prompt
    prompt = f"""你是一个金融分析师。基于以下文档内容回答用户问题。

文档内容：
{context}

用户问题：{question}

要求：
1. 仅基于文档内容回答，不要编造信息
2. 如果文档中没有相关信息，请说"文档中未找到相关信息"
3. 回答要简洁准确，涉及数据时引用具体的原文片段
4. 可以根据文档中的原始数据做基本计算（如毛利率、利润率、同比变化）"""

    # 调用 DeepSeek
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=API_BASE_URL)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    answer = response.choices[0].message.content
    return answer, chunks
