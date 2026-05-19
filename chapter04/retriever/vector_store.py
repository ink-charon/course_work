import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables from .env file
load_dotenv()
PERSIST_DIR = os.getenv("CHROMA_PERSISTENCE","./chroma_db")
EMBED_MODEL = "moka-ai/m3e-base"
embedding_model = SentenceTransformer(EMBED_MODEL)

def get_embedding(text):
    #Generate embedding by using m3e-base
    if not text:
        return []
    try:
        embedding = embedding_model.encode(text)
        return embedding.tolist()
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
    
class ChromaVectorStore:
    def __init__(self, collection_name = "pdf_knowledge_base"):
        # Initialize ChromaDB client and collection
        self.client = chromadb.PersistentClient(
            path = PERSIST_DIR,
            settings = Settings(
                anonymous_telemetry = False,
                allow_reset = True
        )
        )
        self.collection = self.client.get_or_create_collection(
            name = collection_name,
            metadata = {"hnsw:space": "cosine"}
        )
    
    def add_text_chunks(self, chunks):
        #embedding the text chunks and store them in the collection
        if not chunks:
            return
        #1.Generate chunks id
        ids = []
        for i in range(len(chunks)):
            ids.append(f"chunk_{i}")

        #2.transform text chunks into embedding vectors
        embeddings = []
        for chunk in chunks:
            embedding = get_embedding(chunk)
            embeddings.append(embedding)

        #3.filter the empty embedding vectors and corresponding ids
        vaild_ids = []
        for id, emb, chunk in zip(ids, embeddings, chunks):
            if emb:
                vaild_ids.append((id, emb, chunk))

        # check if all of chunks are faild
        if not vaild_ids:
            raise ValueError("All of the text chunks failed to generate embedding. Please check the input text.")

        ids, embeddings, documents = zip(*vaild_ids)

        #4.store to ChromaDB collection
        self.collection.add(
            ids = list(ids),
            embeddings = list(embeddings),
            documents = list(documents)
        )
        print(f"successfully stored{len(vaild_ids)} chunks")

    def similarity_search(self, query, top_k = 5,threshold = 0.7):
        """
        retrieve the similarity text then return the text and similarity scores
        Args:
        query:the text query for retrieval
        top_k:the number of the retrieved results
        threshold:the similarity threshold for filtering results, default is 0.7
        """
        query_embedding = get_embedding(query)
        if not query_embedding:
            return []
        
        #retrive the most similar chunks from the collection
        result = self.collection.query(
            query_embeddings = [query_embedding],
            n_results = top_k,
            include = ["documents", "distances"]
        )
        
        #3.calculate the similarity scores and filter the results based on the threshold
        retrieved_chunks = []
        for doc, dist in zip(result["documents"][0], result["distances"][0]):
            sim = max(0.0,min(1.0,1-dist))

            if sim >= threshold:
                retrieved_chunks.append((doc, sim))
        
        return retrieved_chunks


    def clear_collection(self):
        #clear the collection and reset the ChromaDB
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name = self.collection.name,
            metadata = {"hnsw:space": "cosine"}
        )

if __name__ == "__main__":
    store = ChromaVectorStore()
    text_chunks = ["人工智能是未来的发展方向","深度学习是人工智能的核心技术"]
    store.add_text_chunks(text_chunks)
    print(store.similarity_search("人工智能的核心技术是什么？"))