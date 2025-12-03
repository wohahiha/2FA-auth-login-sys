# crypto_utils.py

# 用于读取 .env 文件中的环境变量
import os
from dotenv import load_dotenv

# 引入对称加密工具 Fernet（基于 AES）
from cryptography.fernet import Fernet

# 加载 .env 文件中的环境变量到系统环境中，再从系统环境变量中获取加密密钥
# .env 文件中包含 FERNET_KEY=xxx
load_dotenv()
FERNET_KEY = os.getenv("FERNET_KEY")

# 从配置文件中获取加密密钥
from config import FERNET_KEY

# 如果没有设置密钥，则抛出错误，防止系统运行在不安全状态
if not FERNET_KEY:
    raise ValueError("未设置 FERNET_KEY")  # 程序启动时必须提供密钥

# 创建 Fernet 对象，用于加密和解密操作
# 该对象将被其他模块（如 user_manager.py、totp_manager.py）导入使用
fernet = Fernet(FERNET_KEY.encode())
