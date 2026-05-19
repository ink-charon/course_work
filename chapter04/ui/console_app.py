"""
控制台应用类 - 主程序入口
协调各个模块完成RAG流程
"""

from retriever.vector_store import ChromaVectorStore
from ui.menu_handler import show_menu, get_user_choice
from knowledge_base.pdf_handler import upload_pdf
from ui.qa_handler import ask_question
from ui.cli_utils import print_section_header

class RAG_ConsoleApp:
    """RAG控制台应用类"""

    def __init__(self):
        """初始化应用"""
        self.vector_store = ChromaVectorStore()
        self.current_pdf = None
        self.chunks_loaded = False

    def handle_upload(self):
        """处理PDF上传"""
        self.current_pdf, success = upload_pdf(self.vector_store)
        if success:
            self.chunks_loaded = True

    def handle_question(self):
        """处理用户提问"""
        ask_question(self.vector_store, self.chunks_loaded)

    def handle_clear(self):
        """处理清空知识库"""
        print_section_header("清空知识库")

        if not self.chunks_loaded:
            print("The knowledge_base already empty!")
            input("\n按回车继续")
            return
        
        confrim = input("确认要清空知识库吗 (y/n)").strip().lower()
        if confrim == 'y':
            try:
                self.vector_store.clear_collection()
                self.current_pdf = None
                self.chunks_loaded = False
                print("知识库已清空")
            except Exception as e:
                print(f"清空失败{e}")
            else:
                print("已取消操作")
                input("\n按回车键继续")

    
    def run(self):
        """运行应用主循环"""

        while True:
            #显示菜单
            show_menu(self.current_pdf, self.chunks_loaded)

            #获取用户选择
            choice = get_user_choice()

            #处理用户选择
            if choice == '1':
                self.handle_upload()
            elif choice == '2':
                self.handle_question()
            elif choice == '3':
                self.handle_clear()
            elif choice == '4':
                print("\n感谢使用RAG问答系统,再见！")
                break
            else:
                print("\n无效选择,请重新输入")
                input("按回车键继续")