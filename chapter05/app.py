import streamlit as st
import os
from core.document_processor import load_file, splitter_documents
from core.vector_store import VectorBaseManager
from core.rag_chain import build_rag_chain
from utils import config

st.set_page_config(page_title="langchain RAG实验",page_icon="📕")
st.title("Langchain RAG智能问答助手")

#初始化会话状态
if "vbm" not in st.session_state:
    st.session_state.vbm = VectorBaseManager()
    #尝试加载已有的向量库
    try:
        st.session_state.vbm.loaded_vectorstore()
        st.sidebar.success(f"已成功加载知识库{st.session_state.vbm.document_count}个文本块")

    except FileNotFoundError:
        st.sidebar.warning("知识库为空,请上传文档")

if "chain" not in st.session_state:
    st.session_state.chain = None

if "k" not in st.session_state:
    st.session_state.k = config.DEFAULT_K
if "threshold" not in st.session_state:
    st.session_state.threshold = config.SIMILARITY_THRESHOLD

#侧边框菜单
menu = st.sidebar.radio(
    "功能选择",
    ["上传文档","智能问答","参数设置","清空知识库"]
)

#上传文档
if menu == "上传文档":
    st.subheader("上传新文档")
    uploaded_file = st.file_uploader(
        "支持PDF、DOC、DOCX、TXT、MD",
        type = ["pdf","docx","txt","doc","md"]
    )
    if uploaded_file is not None:
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path,"wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            docs = load_file(temp_path)
            split_docs = splitter_documents(
            docs,
            chunk_overlap=config.CHUNK_OVERLAP,
            chunk_size=config.CHUNK_SIZE
        )
            vbm = st.session_state.vbm
            vbm.add_documents(split_docs)

            #重建回答链
            st.session_state.chain = build_rag_chain(
                vbm,
                k = st.session_state.k,
                threshold=st.session_state.threshold
            )
            st.success(f"已添加{len(split_docs)}个文本块（总计{vbm.document_count}块）")
        
        except Exception as e:
            st.error(f"处理失败:{e}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

#2.智能问答
elif menu == "智能问答":
    st.subheader("智能问答")
    question = st.text_input("请输入你的问题")
    if question:
        if st.session_state.chain is None:
            st.warning("请先上传文档并构建知识库")
        else:
            with st.spinner("思考中..."):
                answer = st.session_state.chain.invoke(question)
            st.markdown("**回答**")
            st.write(answer)

#3.参数设置
elif menu == "参数设置":
    st.subheader("检索参数调整")
    new_k = st.slider("检索数(k)",1,10,st.session_state.k)
    new_threshold = st.slider("相似度阈值",0.0,1.0,st.session_state.threshold,0.05)

    if st.button("应用新参数"):
        st.session_state.k = new_k
        st.session_state.threshold = new_threshold
        vbm = st.session_state.vbm
        if vbm.vectorstore is not None:
            st.session_state.chain = build_rag_chain(
                vbm, k=new_k,threshold=new_threshold
            )
            st.success(f"参数已更新:k={new_k},阈值={new_threshold}")
        else:
            st.warning("知识库为空，参数将在下次上传文件时生效")

elif menu == "清空知识库":
    st.subheader("清空全部知识库")
    if st.button("确认清空所有文档(不可恢复)"):
        st.session_state.vbm.clear()
        st.session_state.chain = None
        st.success("知识库已清空")