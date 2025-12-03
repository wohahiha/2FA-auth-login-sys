# data_store.py

# 导入标准库模块
import json       # 用于读取和写入 JSON 格式的数据
import os         # 用于文件路径和存在性检查

# 从配置文件中导入用户数据文件路径
from config import USER_DATA_FILE  # 例如：USER_DATA_FILE = "users.json"

def load_users():
    """
    从用户数据文件中加载所有用户信息。
    如果文件不存在或内容无效，返回一个空字典。

    返回值:
        dict: 用户名 -> 用户信息的字典结构
    """
    # 如果用户数据文件不存在，返回空字典
    if not os.path.exists(USER_DATA_FILE):
        return {}

    try:
        # 尝试读取并解析 JSON 文件
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # 如果文件内容不是合法的 JSON，返回空字典（防止程序崩溃）
        return {}

def save_users(users):
    """
    将用户信息保存到用户数据文件中（覆盖写入）。

    参数:
        users (dict): 用户名 -> 用户信息的字典结构
    """
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)  # 使用缩进格式，便于阅读
