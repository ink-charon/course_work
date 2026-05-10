from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self,mdoel_name):
        self.model_name = mdoel_name
        self.model = None

    def load_model(self):
        #加载模型并打印测试句子的嵌入向量维度
        self.model = SentenceTransformer(self.model_name)
        print("模型加载成功,向量为度:",self.encode(["测试句子"])[0].shape)
        return self.model
    
    def encode(self,texts):
        #将文本转换为嵌入向量
        if not self.model:self.load_model()
        return self.model.encode(texts)
    
    def encode_documents(self,documents):
        #将文档转换为嵌入向量
        print("编码文档")
        return self.encode(documents)