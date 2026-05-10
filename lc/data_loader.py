import numpy as np

class DataLoader:
    def __init__(self,config):
        self.config = config
    
    def load_documents(self):
        #加载文档并打印加载多少文档
        documents = self.config["documents"]
        print(f"加载了 {len(documents)} 个文档")
        return documents
    
    def load_test_queries(self):
        #加载测试查询并直接返回
        return self.config["test_query"]
    
    def save_results(self,results,filename="results.txt"):
        #结果保存在文本中，每行一个结果
        with open(filename,"w",encoding="utf-8") as f:
            for query, matches in results.items():
                f.write(f"查询: {query}\n 匹配结果:\n")
                for i, (doc, score) in enumerate(matches, 1):
                    f.write(f"  {i}. {doc} (相似度: {score:.4f})\n")
                f.write("\n")
        print(f"结果已保存到 {filename}")

