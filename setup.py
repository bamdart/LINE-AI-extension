import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

def check_python_version():
    """檢查 Python 版本"""
    if sys.version_info < (3, 8):
        print("需要 Python 3.8 或更高版本")
        sys.exit(1)

def install_requirements():
    """安裝必要的 Python 套件"""
    print("正在安裝必要的 Python 套件...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Python 套件安裝完成！")
    except subprocess.CalledProcessError:
        print("安裝 Python 套件時發生錯誤")
        sys.exit(1)

def check_chrome_extension():
    """檢查 LINE Chrome 擴充功能是否已安裝"""
    extension_id = "ophjlpahpchlmihnnnihgmmeilfjmjjc"
    extension_path = Path(os.path.expanduser("~")) / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Extensions" / extension_id
    
    if not extension_path.exists():
        print("未找到 LINE Chrome 擴充功能")
        print("正在開啟 Chrome 線上應用程式商店...")
        webbrowser.open(f"https://chromewebstore.google.com/detail/line/{extension_id}")
        input("請安裝 LINE 擴充功能後按 Enter 鍵繼續...")
    else:
        print("已找到 LINE Chrome 擴充功能")

def main():
    print("開始安裝程序...")
    
    extension_id = os.getenv("EXTENSION_ID")
    # # 檢查 Python 版本
    # check_python_version()
    
    # # 安裝必要的套件
    # install_requirements()
    
    # 檢查 Chrome 擴充功能
    check_chrome_extension()
    
    print("\n安裝完成！")
    print("您現在可以執行 main.py 來開始監聽 LINE 訊息")
    input("按 Enter 鍵結束安裝程序...")

if __name__ == "__main__":
    main()