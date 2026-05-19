from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Optional
from langchain_core.documents import Document
from utils import config
import os


class VectorBaseManager():
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name = config.EMBEDDING_MODEL,
            model_kwargs ={'device':config.EMBEDDING_DEVICE},
            encode_kwargs ={'normalize_embeddings': True},
            cache_folder=config.EMBEDDING_CACHE_DIR
        )
        self.persist_directory = config.CHROMA_PERSIST_DIRECTORY
        self.collection_name = config.COLLECTION_NAME
        self.vectorstore = None
    def create_from_documents(self,documents:List[Document]):
        """首次从文档列表中创建向量库"""
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        return self.vectorstore
    
    def loaded_vectorstore(self):
        """加载已有的向量库"""
        if not os.path.exists(self.persist_directory):
            raise FileNotFoundError(f"向量库目标{self.persist_directory}不存在")
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function= self.embeddings,
            collection_name=self.collection_name
        )
        return self.vectorstore
    
    def add_documents(self,documents:List[Document]):
        """向已有数据库中添加文档"""
        if self.vectorstore is None:
            #若还没初始化，自动创建
            self.create_from_documents(documents)
        else:
            self.vectorstore.add_documents(documents)
        
    def get_retriever(self,search_type='similarity',k=4,score_threshold=None):
        if self.vectorstore is None:
            raise RuntimeError("向量库尚未初始化，请先创建或加载")
        search_kwargs = {'k':k}
        if search_type == 'similarity_score_threshold':
            search_kwargs['score_threshold'] = score_threshold or 0.5
        elif search_type == 'mmr':
            search_kwargs['fetch_k'] = 20
            search_kwargs['lambda_mult'] = 0.6
        return self.vectorstore.as_retriever(
            search_type = search_type,
            search_kwargs=search_kwargs
        )

    def clear(self):
        """清空当前集合"""
        if self.vectorstore:
            self.vectorstore.delete_collection()
            self.vectorstore = None
    
    @property
    def document_count(self):
        #返回当前集合chunk数量
        if self.vectorstore:
            return self.vectorstore._collection.count()
        return 0