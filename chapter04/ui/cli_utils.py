"""
CLI工具函数
提供控制台相关的辅助功能
"""

import os

def clear_screen():
    """清屏函数，适用于Windows和Unix系统"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_menu_header(title):
    """打印主菜单标题"""
    clear_screen()
    print("=" * 50)
    print(f"{title:^50}")
    print("=" * 50)
    print()

def print_section_header(title):
    """打印章节标题"""
    print("\n" + "-" * 50)
    print(title)
    print("=" * 50)
    print()

def print_divider():
    """打印分割线"""
    print("-" * 50)