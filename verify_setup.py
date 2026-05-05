"""
验证脚本：确认所有工具安装正确
运行方式：python verify_setup.py
"""
import sys
import importlib

packages = [
    ("pandas", "pd"),
    ("numpy", "np"),
    ("matplotlib", "mpl"),
    ("yfinance", "yf"),
    ("openai", "openai"),
    ("langchain", "langchain"),
    ("langgraph", "langgraph"),
    ("chromadb", "chromadb"),
    ("streamlit", "st"),
    ("sklearn", "sklearn"),
    ("xgboost", "xgboost"),
]

print("=" * 50)
print("🎯 AI 金融求职 — 环境验证")
print("=" * 50)

all_ok = True
for pkg_name, alias in packages:
    try:
        mod = importlib.import_module(pkg_name)
        ver = getattr(mod, "__version__", "ok")
        print(f"  ✅ {pkg_name:20s} v{ver}")
    except ImportError as e:
        print(f"  ❌ {pkg_name:20s} 未安装: {e}")
        all_ok = False

print("-" * 50)
if all_ok:
    print("🎉 所有包安装成功！可以开始学习了。")
else:
    print("⚠️ 部分包未安装，请检查上面 ❌ 标记的包。")
print(f"\nPython 版本: {sys.version}")
print("=" * 50)
