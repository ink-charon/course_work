import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

def call_llm_api(prompt):
    """调用LLM API生成回答
    Args:
        prompt (str): 用户输入的提示语
    Returns:
        str: LLM生成的回答
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-v4-pro",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1024
    }
    try:
        resp = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"调用模型失败: {str(e)}"
    

def generate_answer_with_context(query, context_chunks):
    """根据问题和检索到的上下文生成回答
    Args:
        question (str): 用户输入的问题
        context_chunks (list): 检索到的相关文本内容
    Returns:
        str: LLM生成的回答
    """
    context = "\n".join(f"参考资料{i+1}:{chunk[0]}" for i, chunk in enumerate(context_chunks))

    prompt = f"""
你是一个专业的AI助手，帮助用户解答问题。请根据以下参考资料和用户的问题生成一个详细的回答。

参考资料
{context}

规则：
1.仅使用参考资料信息，不能编造信息，
2.如果参考资料中没有相关信息，请直接回答“根据提供的资料无法回答这个问题”，不要编造答案。
3.回答简洁精准，不要包含无关内容。

用户问题：
{query}

回答 :
"""
    
    return call_llm_api(prompt)


def generate_answer_without_context(query):
    """根据问题生成回答（不使用上下文）
    Args:
        question (str): 用户输入的问题
    Returns:
        str: LLM生成的回答
    """
    prompt = f"""
你是一个专业的AI助手，帮助用户解答问题。请根据以下用户的问题生成一个详细的回答。
规则：
1.基于你的知识进行回答问题
2.如果你不知道答案，请直接回答“抱歉，我无法回答这个问题”，不要编造答案。
用户问题：
{query}
回答 :
"""
    return call_llm_api(prompt)

if __name__ == "__main__":
    test_context = [("人工智能是未来的发展方向",0.9), ("深度学习是人工智能的核心技术",0.95)]
    print("测试1 - 基于上下文：")
    print(generate_answer_with_context("人工智能的核心是什么", test_context))
    print()

    #测试2 - 不基于上下文：
    print("测试2 - 不基于上下文：")
    print(generate_answer_without_context("人工智能的核心是什么"))
    