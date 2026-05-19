# RAG 问答系统

基于检索增强生成（Retrieval-Augmented Generation）的 PDF 知识库问答系统。上传 PDF 文档后，系统自动提取、向量化文本内容，支持基于文档内容的智能问答。

## 目录结构

```
chapter04/
├── main.py                   # 程序入口
├── requirements.txt          # 项目依赖
├── .env                      # 环境变量配置
├── knowledge_base/           # 知识库模块
│   ├── pdf_process.py        # PDF 文本提取、清洗、分块
│   └── pdf_handler.py        # PDF 上传与处理流程
├── retriever/                # 检索模块
│   └── vector_store.py       # 向量数据库（ChromaDB + m3e 嵌入模型）
├── generator/                # 生成模块
│   └── generator.py          # 调用 LLM API 生成回答
└── ui/                       # 界面模块
    ├── console_app.py        # 主控制台应用
    ├── menu_handler.py       # 菜单显示与交互
    ├── qa_handler.py         # 问答流程处理
    └── cli_utils.py          # 控制台工具函数
```

## 模块功能

| 模块 | 功能 |
|------|------|
| `knowledge_base/` | PDF 文本提取（PyMuPDF）、文本清洗（修复数字/空格问题）、按句子分块（支持重叠窗口） |
| `retriever/` | 使用 m3e-base 模型将文本转为向量，基于 ChromaDB 存储与余弦相似度检索 |
| `generator/` | 调用 DeepSeek API，支持带上下文（RAG）和不带上下文（纯 LLM）两种生成模式 |
| `ui/` | 控制台交互界面，包括菜单导航、PDF 上传、问答和知识库清空功能 |

## 依赖库

- **chromadb** — 向量数据库，存储和检索文本向量
- **sentence-transformers** — 嵌入模型（moka-ai/m3e-base），将文本转为向量
- **PyMuPDF** — PDF 文件文本提取
- **python-dotenv** — 加载 .env 环境变量
- **requests** — 调用 LLM API

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

在 `.env` 文件中填入你的 API 密钥：

```
DEEPSEEK_API_KEY=你的API密钥
DEEPSEEK_BASE_URL=https://api.deepseek.com
CHROMA_PERSISTENCE=./chroma_db
```

### 3. 运行程序

```bash
python main.py
```

### 4. 操作流程

1. 选择 **上传 PDF 文件**（选项 1），输入 PDF 文件路径
2. 选择 **提问**（选项 2），输入你的问题
3. 系统会检索 PDF 中的相关内容并生成回答
4. 选择 **清除知识库**（选项 3）可清除已加载的文档
5. 选择 **退出**（选项 4）结束程序
