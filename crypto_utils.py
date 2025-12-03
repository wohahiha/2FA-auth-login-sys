# crypto_utils.py

import os
from dotenv import load_dotenv

# 对称加密工具 Fernet
from cryptography.fernet import Fernet

# 加载 .env 文件中的环境变量到系统环境中
load_dotenv()

FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("未设置 FERNET_KEY")
fernet = Fernet(FERNET_KEY.encode())
