# data_store.py

import json
import os

# 导入用户数据文件路径
from config import USER_DATA_FILE

def load_users():
    """
    从用户数据文件中加载所有用户信息。
    如果文件不存在或内容无效，返回一个空字典。

    返回值:
        dict: 用户名 -> 用户信息的字典结构
    """

    if not os.path.exists(USER_DATA_FILE):
        return {}

    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_users(users):
    """
    将用户信息保存到用户数据文件中（覆盖写入）。

    参数:
        users (dict): 用户名 -> 用户信息的字典结构
    """
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
