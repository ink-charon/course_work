import numpy as np

class Retriever:
    def __setup__(self,documents,doc_vectors):
        self.documents = documents
        self.doc_vectors = doc_vectors

    def cosine_similarity(self,vec1,vec2):
        #计算两个向量之间的余弦相似度
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        return dot_product / (norm_vec1 * norm_vec2)
    
    def retrieve(self,query_vector,top_k=3):
        #计算查询向量与文档向量之间的相似度，返回相似度最高的前top_k个文档
        similarity = [(i,self.cosine_similarity(query_vector, vec))
                      for i, vec in enumerate(self.doc_vectors)]
        similarity.sort(key=lambda x: x[1], reverse=True)
        return [(self.documents[idx], score) for idx, score in similarity[:top_k]]