# logger.py

import json  # 用于读写 JSON 格式的日志文件
import os  # 用于检查文件是否存在
from datetime import datetime  # 用于生成当前时间戳
from config import LOG_FILE  # 从配置文件中导入日志文件路径（如 "login_logs.json"）


def log_login_attempt(username, success, reason=None, device_id=None):
    """
    记录一次登录尝试的日志信息。

    参数:
        username (str): 尝试登录的用户名
        success (bool): 登录是否成功
        reason (str): （可选）失败原因，如 "密码错误"
        device_id (str): （保留字段）设备标识，用于未来支持“记住设备”等功能
    """

    # 构建一条日志记录（字典格式）
    log_entry = {
        "username": username,
        "success": success,
        "reason": reason,
        # "device_id": device_id,  # 预留字段，暂未使用
        "timestamp": datetime.now().isoformat()  # 当前时间，ISO 格式
    }

    logs = []

    # 如果日志文件存在，尝试读取已有日志
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)  # 读取并解析为列表
            except json.JSONDecodeError:
                # 如果文件损坏或为空，初始化为空列表
                logs = []

    # 将新的日志记录添加到日志列表中
    logs.append(log_entry)

    # 写回日志文件（格式化缩进，便于阅读）
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)


def get_logs():
    """
    获取所有登录日志记录（用于调试或后台查看）。

    返回:
        list[dict]: 日志记录列表
    """
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
