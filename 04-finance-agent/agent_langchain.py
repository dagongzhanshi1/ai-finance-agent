"""agent_langchain.py - LangChain 版金融 Agent（新版 API）"""
import os
import sys
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools_def import ALL_TOOLS

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)

agent = create_agent(
    model=llm,
    tools=ALL_TOOLS,
    system_prompt="你是一个金融数据助手。根据用户的问题调用对应的工具来获取数据，然后用数据回答用户。",
    debug=True,
)


if __name__ == "__main__":
    user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("你想查什么？")
    result = agent.invoke({"messages": [("user", user_input)]})
    print(result["messages"][-1].content)
