"""
菜单处理模块
负责显示菜单和处理用户选择
"""

from ui.cli_utils import clear_screen, print_menu_header

def show_menu(current_pdf, chunks_loaded):
    """显示主菜单并处理用户选择
    Args:
        current_pdf: 当前加载的PDF文件名
        chunks_loaded: 是否已加载文本块
    """

    clear_screen()
    print_menu_header("RAG问答系统 - 控制台版本")

    #显示当前状态
    if current_pdf:
        print(f"当前PDF文件: {current_pdf}")
        print(f"文本块加载状态: {'已加载' if chunks_loaded else '未加载'}")
    else:
        print("当前知识库状态: 未加载")

    print()
    print("请选择操作:")
    print("1. 上传PDF文件(输入文件路径)")
    print("2.提问")
    print("3.清除知识库")
    print("4.退出")
    print("="*50)

def get_user_choice():
    """获取用户选择
    Returns:
        用户输入的选择
    """

    return input("请输入选项编号: ").strip()