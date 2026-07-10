"""cli.py - 命令行入口：python cli.py 600519"""
import sys
import logging

from workflow import app, logger

if __name__ == "__main__":
    # 取命令行参数，没传就手动输入
    user_input = sys.argv[1] if len(sys.argv) > 1 else input("输入股票代码（600519 或 002594）：")

    logger.info(f"===== 工作流启动：{user_input} =====")
    result = app.invoke({
        "symbol": user_input,
        "stock_info": None,
        "financial_info": None,
        "news": None,
        "report": None,
    })
    logger.info(f"===== 工作流结束 =====")

    print("\n" + "=" * 40)
    print(result["report"])
    if result.get("token_usage"):
        print(f"\n--- {result['token_usage']} ---")
