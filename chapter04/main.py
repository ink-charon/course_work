from ui.console_app import RAG_ConsoleApp

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print(" RAG问答系统 -- 控制台版本")
    print("=" * 60)
    print("\正在初始化")
    print("加载嵌入模型（首次运行会自动下载）")
    print(" - 初始化向量数据库")
    print("\n请稍后")

    try:
        app = RAG_ConsoleApp()
        print("\n初始化完成")
        input("按回车继续")
        app.run()
    except KeyboardInterrupt:
        print("\n\n程序已退出")
    except Exception as e:
        print(f"初始化失败{str(e)}")
        print("\n\n请检查:")
        print("1.是否安装了所有依赖:pip install -r requirements.txt")
        print("2..env是否配置完整")
        input("\n按回车键退出")