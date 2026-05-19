import os
from dotenv import load_dotenv

load_dotenv()
#嵌入模型
EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"
EMBEDDING_DEVICE = "cpu"
EMBEDDING_CACHE_DIR = "./models/embeddings" 

#向量库
CHROMA_PERSIST_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "default"

#文本切割
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

#检索
DEFAULT_K = 3
SIMILARITY_THRESHOLD = 0.6

#LLM
LLM_MODEL = "deepseek-v4-flash"
LLM_API_KEY = os.getenv("DEEPSEEK_API_KEY")
LLM_BASE_URL = os.getenv("BASE_URL")
LLM_TEMPERATURE = 0.7