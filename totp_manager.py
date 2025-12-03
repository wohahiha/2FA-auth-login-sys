# totp_manager.py

# 导入 TOTP 库（基于时间的一次性密码，符合 RFC 6238）
import pyotp

# 用于生成二维码图像（用于绑定 Authenticator 应用）
import qrcode

# 用于获取当前时间戳
from datetime import datetime

# 导入用户数据获取函数
from user_manager import get_user

# 导入 Fernet 加密器（用于加密 TOTP 密钥）
from crypto_utils import fernet


def generate_secret():
    """
    生成一个新的 TOTP 密钥（Base32 编码）。

    返回:
        str: 用于绑定 Authenticator 的密钥
    """
    return pyotp.random_base32()


def encrypt_secret(secret):
    """
    使用 Fernet 加密 TOTP 密钥。

    参数:
        secret (str): 原始 TOTP 密钥
    返回:
        str: 加密后的密钥字符串
    """
    return fernet.encrypt(secret.encode()).decode()


def decrypt_secret(enc_secret):
    """
    解密加密的 TOTP 密钥。

    参数:
        enc_secret (str): 加密后的密钥
    返回:
        str: 原始 TOTP 密钥
    """
    return fernet.decrypt(enc_secret.encode()).decode()


def get_decrypted_secret(user):
    """
    从用户数据中获取解密后的 TOTP 密钥。

    参数:
        user (dict): 用户对象
    返回:
        str: 解密后的 TOTP 密钥
    """
    return decrypt_secret(user["secret"])


def generate_qr_code(username, secret, issuer="MyApp"):
    """
    生成并显示绑定二维码（用于 Google Authenticator、Microsoft Authenticator 等）。

    参数:
        username (str): 用户名
        secret (str): TOTP 密钥
        issuer (str): 应用名称（在 Authenticator 中显示）
    """
    # 生成 otpauth URI
    uri = pyotp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer)

    # 使用 qrcode 库生成二维码图像
    qr = qrcode.make(uri)

    # 显示二维码（弹出窗口）
    qr.show()


def verify_code(secret, code, last_used_time=None):
    """
    验证用户输入的 TOTP 验证码是否正确。

    参数:
        secret (str): TOTP 密钥
        code (str): 用户输入的验证码
        last_used_time (int): 上次验证时的时间戳（用于防止重放）

    返回:
        (bool, int): 验证是否成功，当前时间戳
    """
    totp = pyotp.TOTP(secret)
    current_time = totp.timecode(datetime.now())

    # 防止重放攻击（重复使用相同时间段的验证码）
    if last_used_time and current_time == last_used_time:
        return False, current_time

    # 验证验证码是否有效（默认容差为 ±30 秒）
    if totp.verify(code):
        return True, current_time
    return False, current_time


def get_totp(username):
    """
    获取指定用户的 TOTP 对象（用于验证）。

    参数:
        username (str)
    返回:
        pyotp.TOTP 或 None
    """
    user = get_user(username)
    if not user:
        return None

    secret = get_decrypted_secret(user)
    return pyotp.TOTP(secret)


def verify_totp(username, input_code):
    """
    验证指定用户的 TOTP 验证码是否正确。

    参数:
        username (str)
        input_code (str): 用户输入的验证码
    返回:
        bool: 是否验证成功
    """
    totp = get_totp(username)
    if not totp:
        return False
    return totp.verify(input_code)
