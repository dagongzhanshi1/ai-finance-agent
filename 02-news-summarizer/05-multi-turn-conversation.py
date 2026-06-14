"""
Day 22 — 多轮对话记忆

演示两个概念：
1. 无记忆：每次对话独立，模型不记得之前说了什么 ❌
2. 有记忆：手动维护消息列表，让对话有上下文 ✅
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

MODEL = "deepseek-chat"

# ============================================================
# 第一部分：不加记忆的问题
# ============================================================

print("=" * 50)
print("第一部分：无记忆 — 每次对话独立")
print("=" * 50)

# 第一次调用：告诉模型我的名字
messages_1 = [{"role": "user", "content": "我的名字是张三，我是做量化分析的。"}]
resp_1 = client.chat.completions.create(model=MODEL, messages=messages_1)
print("第1次调用：", resp_1.choices[0].message.content[:100])

# 第二次调用：问名字 — 但消息列表是全新的，模型不知道
messages_2 = [{"role": "user", "content": "我叫什么名字？"}]
resp_2 = client.chat.completions.create(model=MODEL, messages=messages_2)
print("第2次调用：", resp_2.choices[0].message.content[:150])

print()
print("❌ 第二次调用完全不知道之前说过什么，因为每次都是独立的消息列表。")
print()

# ============================================================
# 第二部分：手动维护历史
# ============================================================

print("=" * 50)
print("第二部分：手动管理消息历史 ✅")
print("=" * 50)


class Conversation:
    """一个能记住上下文的多轮对话管理器。"""

    def __init__(self, system_prompt=None):
        # 初始化消息列表，可选的 system prompt 在最前面
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def chat(self, user_input):
        """发送用户消息，得到回复，并自动保存到历史中。"""
        # 1. 把用户的消息加到历史列表
        self.messages.append({"role": "user", "content": user_input})

        # 2. 把整个历史发给 API
        response = client.chat.completions.create(
            model=MODEL,
            messages=self.messages
        )

        # 3. 取出模型的回复
        reply = response.choices[0].message.content

        # 4. 把模型的回复也存到历史（这样下一轮才能"记住"）
        self.messages.append({"role": "assistant", "content": reply})

        return reply

    def get_history(self):
        """查看当前的对话历史（调试用）。"""
        for i, msg in enumerate(self.messages):
            print(f"  [{i}] {msg['role']}: {msg['content'][:80]}...")


# ——— 测试 Conversation 类 ———

conv = Conversation(system_prompt="你是金融分析助手，回答要简洁。")

print("\n▶ 第1轮：告诉名字")
reply_1 = conv.chat("我的名字是张三，我是做量化分析的。")
print(f"  模型说：{reply_1[:120]}")

print("\n▶ 第2轮：问名字 — 应该记得")
reply_2 = conv.chat("你记得我叫什么名字吗？我做什么工作？")
print(f"  模型说：{reply_2[:120]}")

print("\n▶ 第3轮：进一步提问")
reply_3 = conv.chat("那量化分析一般用什么编程语言？")
print(f"  模型说：{reply_3[:120]}")

print("\n▶ 当前对话历史")
conv.get_history()
