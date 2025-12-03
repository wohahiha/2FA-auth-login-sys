# logger.py

import json
import os
from datetime import datetime
from config import LOG_FILE  # 导入日志文件路径


def log_login_attempt(username, success, reason=None, device_id=None):
    """
    记录一次登录尝试的日志信息。

    参数:
        username (str): 尝试登录的用户名
        success (bool): 登录是否成功
        reason (str): （可选）失败原因，如 "密码错误"
        device_id (str): （保留字段）设备标识，用于未来支持“记住设备”等功能
    """

    log_entry = {
        "username": username,
        "success": success,
        "reason": reason,
        # "device_id": device_id,
        "timestamp": datetime.now().isoformat()  # 当前时间，ISO 格式
    }

    logs = []

    # 尝试读取已有日志
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    # 添加日志
    logs.append(log_entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)


def get_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
