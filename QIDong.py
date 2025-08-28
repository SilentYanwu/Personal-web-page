# 导入必要的模块
import http.server  # Python内置的HTTP服务器模块
import socketserver # 提供更高级的套接字服务器功能
import webbrowser   # 用于控制浏览器打开网页
import threading    # 多线程支持，用于后台运行服务器
import time         # 时间控制相关功能
import os           # 操作系统接口，用于文件路径检查

# 配置常量
PORT = 8000          # 服务器监听的端口号（可修改）
DIRECTORY = "."      # 网页文件所在的目录（.表示当前目录）
TARGET_FILE = "Me.html"  # 要打开的特定网页文件

# 定义服务器启动函数
def start_server():
    # 创建自定义请求处理器，继承自SimpleHTTPRequestHandler
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            # 调用父类构造函数，指定服务目录
            super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    # 创建TCP服务器实例
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        # 打印服务器启动信息
        print(f"✅ 本地服务器已启动")
        print(f"🌐 访问地址: http://localhost:{PORT}/{TARGET_FILE}")
        print("🛑 按 Ctrl+C 停止服务器")
        # 启动服务器，使其持续运行
        httpd.serve_forever()

# 主程序入口
if __name__ == "__main__":
    # ================= 文件检查部分 =================
    # 检查目标文件是否存在（关键应用：防止启动不存在的文件）
    if not os.path.exists(TARGET_FILE):
        # 如果文件不存在，打印错误信息
        print(f"❌ 错误：找不到文件 {TARGET_FILE}")
        print("请确保：")
        print(f"1. {TARGET_FILE} 文件存在")
        print(f"2. 运行脚本与 {TARGET_FILE} 在同一目录")
        exit(1)  # 退出程序，错误代码1
    
    # ================= 服务器启动部分 =================
    # 创建后台线程运行服务器（关键应用：不阻塞主线程）
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # 设置为守护线程（主程序退出时自动结束）
    server_thread.start()  # 启动线程
    
    # 给服务器启动留一点时间（关键应用：确保服务器准备好再打开浏览器）
    time.sleep(0.5)  # 0.5秒等待时间
    
    # ================= 浏览器控制部分 =================
    # 自动打开特定网页文件（核心功能：一键打开目标网页）
    webbrowser.open(f"http://localhost:{PORT}/{TARGET_FILE}")
    
    # ================= 主线程控制部分 =================
    # 保持主线程运行（关键应用：防止程序立即退出）
    try:
        print(f"⏳ 正在打开 {TARGET_FILE}...")
        # 无限循环保持程序运行（每秒休眠一次）
        while True:
            time.sleep(1)
    # 捕获键盘中断信号（Ctrl+C）
    except KeyboardInterrupt:
        print("\n🚫 服务器已停止")  # 打印停止信息