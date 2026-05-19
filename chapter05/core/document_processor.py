import os
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from typing import List
from langchain_core.documents import Document
#加载文件
def load_file(file_path):
    ext = Path(file_path).suffix.lower()
    if not os.path.exists(file_path):
        raise FileNotFoundError("文件不存在")
    
    loader_map = {
        '.doc': Docx2txtLoader,
        '.docx': Docx2txtLoader,
        '.pdf': PyMuPDFLoader,
        '.md' : TextLoader,
        '.txt': TextLoader
    }
    LoaderCls = loader_map.get(ext)
    if not LoaderCls:
        raise ValueError(f"不支持的文件格式:{ext}")
    
    if ext in ['.txt','.md']:
        loader = LoaderCls(file_path, encoding='utf-8')
    else:
        loader = LoaderCls(file_path)
    return loader.load()

#分割文本
def splitter_documents(documents:List[Document],chunk_size=500,chunk_overlap=50) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_overlap=chunk_overlap,
        chunk_size=chunk_size,
        separators=["\n\n","\n","。","，","？","！","；"]
    )
    return splitter.split_documents(documents)