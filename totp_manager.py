# totp_manager.py


import pyotp
import qrcode
from datetime import datetime
from user_manager import get_user

# 导入 Fernet 加密器
from crypto_utils import fernet


def generate_secret():
    return pyotp.random_base32()


def encrypt_secret(secret):
    return fernet.encrypt(secret.encode()).decode()


def decrypt_secret(enc_secret):
    return fernet.decrypt(enc_secret.encode()).decode()


def get_decrypted_secret(user):
    """
    从用户数据中获取解密后的 TOTP 密钥。
    """
    return decrypt_secret(user["secret"])


def generate_qr_code(username, secret, issuer="MyApp"):
    # 生成 otpauth URI
    uri = pyotp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer)

    qr = qrcode.make(uri)
    qr.show()


def verify_code(secret, code, last_used_time=None):
    """
    验证用户输入的 TOTP 验证码是否正确。
    """
    totp = pyotp.TOTP(secret)
    current_time = totp.timecode(datetime.now())

    # 防止重放攻击
    if last_used_time and current_time == last_used_time:
        return False, current_time

    # 验证验证码是否有效（默认容差为 ±30 秒）
    if totp.verify(code):
        return True, current_time
    return False, current_time


def get_totp(username):
    """
    获取指定用户的 TOTP 对象（用于验证）。
    """
    user = get_user(username)
    if not user:
        return None

    secret = get_decrypted_secret(user)
    return pyotp.TOTP(secret)


def verify_totp(username, input_code):
    """
    验证指定用户的 TOTP 验证码是否正确。
    """
    totp = get_totp(username)
    if not totp:
        return False
    return totp.verify(input_code)
