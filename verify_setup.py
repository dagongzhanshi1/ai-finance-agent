"""
验证脚本：确认所有工具安装正确
运行方式：python3 verify_setup.py
"""
import sys
import importlib

packages = [
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("matplotlib", "matplotlib"),
    ("seaborn", "seaborn"),
    ("yfinance", "yfinance"),
    ("openai", "openai"),
    ("dotenv", "python-dotenv"),
    ("pydantic", "pydantic"),
    ("streamlit", "streamlit"),
    ("pdfplumber", "pdfplumber"),
    ("chromadb", "chromadb"),
    ("langchain_text_splitters", "langchain-text-splitters"),
    ("sentence_transformers", "sentence-transformers"),
]

print("=" * 50)
print("AI 金融求职 - 环境验证")
print("=" * 50)

all_ok = True
for import_name, package_name in packages:
    try:
        mod = importlib.import_module(import_name)
        ver = getattr(mod, "__version__", "ok")
        print(f"  [OK]   {package_name:28s} v{ver}")
    except ImportError as e:
        print(f"  [MISS] {package_name:28s} 未安装: {e}")
        all_ok = False

print("-" * 50)
if all_ok:
    print("所有包安装成功，可以运行阶段 1-3 项目。")
else:
    print("部分包未安装，请先运行：pip install -r requirements.txt")
print(f"\nPython 版本: {sys.version}")
print("=" * 50)
