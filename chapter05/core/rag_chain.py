from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from core.vector_store import VectorBaseManager
from utils import config

def format_docs(docs):
    return "\n\n".join(
        f"【来源:{doc.metadata.get('source','未知')}】 \n{doc.page_content}"
        for doc in docs
    )

def build_rag_chain(vbm:VectorBaseManager,k=4,threshold=0.7):
    retriever = vbm.get_retriever(
        search_type='similarity_score_threshold',
        k=k,
        score_threshold=threshold
    )
    llm = ChatOpenAI(
        model = config.LLM_MODEL,
        api_key= config.LLM_API_KEY,
        base_url=config.LLM_BASE_URL,
        temperature=config.LLM_TEMPERATURE
    )

    template = """
    基于以下上下文回答问题，若找不到答案请直接回答不知道，不要虚构答案。

    上下文
    {context}

    问题：{question}

    回答："""
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context":retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain