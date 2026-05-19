"""
问答处理模块
负责处理用户提问和生成回答
"""
from generator.generator import generate_answer_with_context, generate_answer_without_context
from ui.cli_utils import print_section_header, print_divider

def get_user_question():
    """
    获取用户输入的问题

    返回：
        str: 用户输入的问题,如果用户想要返回主菜单则返回None
    """
    print("请输入您的问题,或输入'quit'返回主菜单")
    query = input("问题: ").strip()
    if not query or query.lower() == 'quit':
        return None
    return query

def search_knowledge_base(query, vector_store):
    """
    在知识库中检索相关内容

    参数:
        query (str): 用户输入的问题
        vector_store (ChromaVectorStore): 向量数据库实例

    返回:
        list: 检索到的相关文本内容列表，格式为[(文本内容, 相关度), ...]
    """
    print(f"\n正在检索与问题相关的内容...")

    try:
        context_chunks = vector_store.similarity_search(query, top_k=3)
        return context_chunks
    except Exception as e:
        print(f"检索失败: {str(e)}")
        input("按回车键返回主菜单...")
        return None


def generate_answer(query, context_chunks):
    """
    根据用户问题和检索到的上下文生成回答
    参数:
        query (str): 用户输入的问题
        context_chunks (list): 检索到的相关文本内容列表，格式为[(文本内容, 相关度), ...]
    
    返回:
        
        str: LLM生成的回答
    
    """
    if not context_chunks:
        print("在知识库中未找到相关信息")
        print("\n正在使用大模型直接回答问题...")
        answer = generate_answer_without_context(query)
    else:
        print("在知识库中找到问题相关的信息，正在生成回答...")
        answer = generate_answer_with_context(query, context_chunks)

    return answer

def display_answer(answer):
    """
    显示生成的回答

    参数:
        answer (str): LLM生成的回答
    """
    print("\n")
    print_divider()
    print("回答:")
    print_divider()
    print(answer)
    print_divider()
    input("按回车键返回主菜单...")

def ask_question(vector_store, chunks_loaded):
    """
    处理用户提问
    Args:
    vector_store (ChromaVectorStore): 向量数据库实例
    chunks_loaded (bool): 是否已经加载了文本块
    """
    #检查是否上传了PDF文档
    if not chunks_loaded:
        print("请先上传PDF文档")
        input("按回车键返回主菜单...")
        return
    
    query = get_user_question()
    if query is None:
        return
    
    #搜索知识库
    context_chunks = search_knowledge_base(query, vector_store)
    if context_chunks is None:
        return
    
    #生成回答
    answer = generate_answer(query, context_chunks)
    #显示回答
    display_answer(answer)