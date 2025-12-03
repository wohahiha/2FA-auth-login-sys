# user_manager.py

import time
import hashlib
import secrets

# 导入数据读写模块
from data_store import load_users, save_users

# 导入对称加密器
from crypto_utils import fernet

# 导入配最大失败次数、锁定时长
from config import MAX_FAILED_ATTEMPTS, LOCK_DURATION


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(username, secret, password, email=None, phone=None):
    """
    添加新用户并保存到 users.json 文件中。
    参数:
        username (str): 用户名
        secret (str): TOTP 密钥（未加密）
        password (str): 明文密码
        email (str): 可选邮箱
        phone (str): 可选手机号
    异常:
        ValueError: 用户已存在
    """
    users = load_users()

    if username in users:
        raise ValueError("用户已存在")

    users[username] = {
        "secret": fernet.encrypt(secret.encode()).decode(),  # 加密 TOTP 密钥
        "password": hash_password(password),
        "email": email,
        "phone": phone,
        "recovery_codes": generate_recovery_codes(),
        "failed_attempts": 0,
        "locked_until": 0,
        "last_verified_time": 0,                             # 上次验证时间（保留字段）
        "verification_codes": {}
    }

    save_users(users)


def get_user(username):
    return load_users().get(username)


def get_remaining_attempts(username):
    """
    获取用户剩余的登录尝试次数。
    """
    users = load_users()
    if username in users:
        return max(0, MAX_FAILED_ATTEMPTS - users[username].get("failed_attempts", 0))
    return MAX_FAILED_ATTEMPTS


def is_user_locked(user):
    return time.time() < user.get("locked_until", 0)


def lock_user(username):
    users = load_users()
    if username in users:
        users[username]["locked_until"] = time.time() + LOCK_DURATION
        save_users(users)


def reset_failed_attempts(username):
    """
    重置用户的失败尝试次数。
    """
    users = load_users()
    if username in users:
        users[username]["failed_attempts"] = 0
        save_users(users)


def increment_failed_attempts(username):
    """
    增加用户的失败尝试次数。
    """
    users = load_users()
    if username in users:
        users[username]["failed_attempts"] += 1
        save_users(users)


def verify_password(user, input_password):
    return hash_password(input_password) == user.get("password")


def generate_recovery_codes(n=5):
    return [secrets.token_hex(4) for _ in range(n)]


def verify_recovery_code(username, code):
    users = load_users()
    user = users.get(username)
    if not user:
        return False

    if code in user.get("recovery_codes", []):
        user["recovery_codes"].remove(code)  # 恢复码只能一次性使用
        save_users(users)
        return True

    return False
