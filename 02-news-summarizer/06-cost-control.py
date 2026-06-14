"""
Day 23 — Token 成本控制

演示三个概念：
1. 看每次调用花了多少 token
2. 算花了多少钱
3. 怎么省钱（max_tokens + 截断历史）
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

# DeepSeek V4 Flash 价格（官方定价，2026年5月25日）
# 来源：https://api-docs.deepseek.com/quick_start/pricing
# 单位：人民币(元) / 1M tokens
PRICE_PROMPT = 1.0       # 输入（缓存未命中）：1元 / 1M tokens
PRICE_COMPLETION = 2.0   # 输出：2元 / 1M tokens
# 缓存命中价：0.02元 / 1M tokens（缓存命中时自动享受，无需额外配置）

# ============================================================
# 第一部分：看每次调用用了多少 token
# ============================================================

print("=" * 60)
print("第一部分：查看每次调用的 token 消耗")
print("=" * 60)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "你是金融分析助手。"},
        {"role": "user", "content": "请用三句话解释什么是市盈率（PE）。"}
    ]
)

usage = response.usage
print(f"\n输入 token (prompt):     {usage.prompt_tokens}")
print(f"输出 token (completion): {usage.completion_tokens}")
print(f"总 token:                {usage.total_tokens}")

# 算钱
cost = (usage.prompt_tokens / 1_000_000 * PRICE_PROMPT +
        usage.completion_tokens / 1_000_000 * PRICE_COMPLETION)
print(f"本次调用花费:            ¥{cost:.6f}")

reply = response.choices[0].message.content
print(f"\n模型回答:\n{reply}")
print()

# ============================================================
# 第二部分：加长输入 vs 加长输出，成本差多少
# ============================================================

print("=" * 60)
print("第二部分：输入长 vs 输出长，成本差多少")
print("=" * 60)

# 测试1：长输入（给一篇长文章让模型总结）
long_article = "贵州茅台是A股市场最具代表性的消费龙头股。" * 50  # 重复50次，造出长输入

resp_long_input = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "你是金融分析助手。"},
        {"role": "user", "content": f"帮我总结一下这篇文章的核心观点：{long_article}"}
    ],
    max_tokens=100  # 限制输出长度
)
u1 = resp_long_input.usage
cost1 = (u1.prompt_tokens / 1_000_000 * PRICE_PROMPT +
         u1.completion_tokens / 1_000_000 * PRICE_COMPLETION)
print(f"\n长输入({u1.prompt_tokens} tokens) + 短输出({u1.completion_tokens} tokens)")
print(f"  花费: ¥{cost1:.6f}")

# 测试2：短输入 + 长输出（简单问题但要详细回答）
resp_long_output = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "你是金融分析助手。"},
        {"role": "user", "content": "什么是市盈率？请非常详细地解释，不少于500字。"}
    ]
)
u2 = resp_long_output.usage
cost2 = (u2.prompt_tokens / 1_000_000 * PRICE_PROMPT +
         u2.completion_tokens / 1_000_000 * PRICE_COMPLETION)
print(f"\n短输入({u2.prompt_tokens} tokens) + 长输出({u2.completion_tokens} tokens)")
print(f"  花费: ¥{cost2:.6f}")

# 对比结论
print(f"\n对比：输出 token 的费用是输入的 {PRICE_COMPLETION/PRICE_PROMPT:.0f} 倍")
print("所以让模型说太多话比给它看很多材料更贵！")

# ============================================================
# 第三部分：历史累积成本（模拟多轮对话）
# ============================================================

print("\n" + "=" * 60)
print("第三部分：多轮对话的累积成本")
print("=" * 60)


class CostAwareConversation:
    """跟 Day 22 的 Conversation 一样，但记录每次花费"""

    def __init__(self, system_prompt=None):
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
        self.total_cost = 0.0
        self.rounds = []

    def chat(self, user_input, max_tokens=None):
        self.messages.append({"role": "user", "content": user_input})

        kwargs = {"model": MODEL, "messages": self.messages.copy()}
        if max_tokens:
            kwargs["max_tokens"] = max_tokens

        response = client.chat.completions.create(**kwargs)

        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})

        # 算本次花费
        u = response.usage
        cost = (u.prompt_tokens / 1_000_000 * PRICE_PROMPT +
                u.completion_tokens / 1_000_000 * PRICE_COMPLETION)
        self.total_cost += cost
        self.rounds.append({
            "prompt_tokens": u.prompt_tokens,
            "completion_tokens": u.completion_tokens,
            "total_tokens": u.total_tokens,
            "cost": cost
        })

        return reply


# 模拟 5 轮对话
conv = CostAwareConversation(system_prompt="你是金融分析助手，回答要简洁。")

questions = [
    "什么是市盈率？",
    "市净率又是什么？",
    "那 ROE 跟这两个指标有什么关系？",
    "能举个用这三个指标分析公司的例子吗？",
    "茅台的 PE 和 PB 大概是多少？"
]

for i, q in enumerate(questions):
    print(f"\n--- 第{i+1}轮 ---")
    reply = conv.chat(q)
    r = conv.rounds[i]
    print(f"  prompt: {r['prompt_tokens']} tokens | "
          f"completion: {r['completion_tokens']} tokens | "
          f"cost: ¥{r['cost']:.6f}")
    print(f"  回答: {reply[:80]}...")

print(f"\n{'='*60}")
print(f"5 轮对话总成本: ¥{conv.total_cost:.6f}")
print(f"最后一轮的消息列表长度: {len(conv.messages)} 条消息")
print(f"最后一轮的 prompt tokens: {conv.rounds[-1]['prompt_tokens']}")
print(f"→ 随着对话变长，每次 prompt 的 token 越来越多，成本也在增长")

# ============================================================
# 第四部分：怎么省钱
# ============================================================

print("\n" + "=" * 60)
print("第四部分：省钱技巧")
print("=" * 60)

print("""
1. max_tokens 设上限
   → 控制模型不要长篇大论。如 max_tokens=200

2. system prompt 精简
   → 系统提示每多 100 token，每 1 万次调用就多花 1 元

3. 历史太长时做截断
   → 只保留最近 N 轮对话，把最早的消息删掉
   → 示例：self.messages = self.messages[-20:]（保留最近 20 条）

4. 便宜的模型做简单任务
   → 摘要/分类用便宜的模型，复杂推理用贵的
   → DeepSeek V4 Flash 性价比很高

5. 缓存重复请求
   → 同一篇新闻不要每次都调 API
   → DeepSeek 缓存命中价仅 0.02 元/百万 token
""")

# 演示截断的效果：把旧对话去掉后，prompt tokens 会减少
print("-" * 60)
print("演示截断对 token 的影响：")
print(f"  Day 22 的 5 轮对话后, prompt 从 ~{conv.rounds[0]['prompt_tokens']} 涨到 ~{conv.rounds[-1]['prompt_tokens']} tokens")
print(f"  如果只保留最近 3 轮，prompt 大约能省 40%")
