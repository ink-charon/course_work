# LC — 基于 BGE 的中文文档检索实验

## 模块说明

| 文件 | 作用 |
|------|------|
| `config.py` | 配置文件，定义文档列表、测试查询和模型名称 |
| `data_loader.py` | 数据加载模块，负责加载文档、测试查询，以及将结果保存到文本文件 |
| `embedder.py` | 编码模块，基于 sentence-transformers 加载 BGE 模型，将文本编码为稠密向量 |
| `retriever.py` | 检索模块，对查询向量和文档向量进行余弦相似度计算并排序，返回 Top-K 匹配结果 |
| `main.py` | 主入口，串联"加载文档 → 编码 → 检索 → 输出结果"的完整流程 |

## 数据流

```
config.py → DataLoader.load_documents() → Embedder.encode_documents()
                                         → Embedder.encode(queries)
                                         → Retriever.search() → 打印结果
```

## 使用方法

1. 将 BGE 模型文件放入 `./bge-small-zh-v1.5/` 目录
2. 在 `config.py` 中配置文档列表和测试查询
3. 运行主程序：

```bash
python main.py
```

## 依赖库

| 库 | 版本 |
|----|------|
| Python | ≥3.10 |
| torch | ≥2.0.0 |
| transformers | ≥4.30.0 |
| sentence-transformers | ≥5.0.0 |
| numpy | ≥1.24.0 |
