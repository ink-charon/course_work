import numpy as np
from retriever import Retriever
from data_loader import DataLoader
from embedder import Embedder
from config import CONFIG
def main():
    print("开始加载数据...")
    data_loader = DataLoader(CONFIG)
    documents = data_loader.load_documents()
    queries = data_loader.load_test_queries()
    #加载模型与编码文档
    embedder = Embedder(CONFIG["model_name"])
    doc_vectors = embedder.encode_documents(documents)
        
    #创建检索器并进行检索
    retriever = Retriever()
    retriever.__setup__(documents, doc_vectors)
    
    #查询编码并检索 
    query_vectors = embedder.encode(queries)
    all_results = {}
    for query, vec in zip(queries, query_vectors):
        print(f"\n 查询: {query} \n最相关的文档:")
        results = retriever.retrieve(vec, top_k=CONFIG["top_k"])
        for i,(doc, score) in enumerate(results,1):
            print(f" {i}. {doc} (相似度: {score:.4f})\n文档:{doc[:50]}...") #显示文档前50个字符
        all_results[query] = results


    #保存结果
    data_loader.save_results(all_results)
    avg_sims = [np.mean([score for _, score in matches]) for matches in all_results.values()]
    print("\n" + "="*50 + "\n 实验完成"+"\n"+"="*50)

if __name__ == "__main__":
    main()