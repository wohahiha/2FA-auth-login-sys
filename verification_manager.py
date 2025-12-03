# verification_manager.py

import secrets
import time
from email.header import Header
from config import VERIFICATION_CODE_EXPIRY
from data_store import load_users, save_users
from user_manager import get_user, verify_password
from config import EMAIL_SENDER, EMAIL_PASSWORD, TWILIO_SID, TWILIO_TOKEN, TWILIO_PHONE
from email.mime.text import MIMEText
import smtplib
from twilio.rest import Client


def generate_code():
    """
    生成 6 位数字验证码（100000 ~ 999999）。
    """
    return str(secrets.randbelow(900000) + 100000)


def send_code(contact, method, is_registration=False):
    """
    发送验证码并根据阶段决定是否写入用户数据。
    """
    code = generate_code()
    timestamp = time.time()

    # 发送验证码
    if method == "email":
        send_email_code(contact, code)
    elif method == "sms":
        send_sms_code(contact, code)
    else:
        raise ValueError("不支持的发送方式")

    if is_registration:
        # 注册阶段：不写入文件，只返回验证码对象，GUI 内存中验证
        return {"code": code, "timestamp": timestamp}

    # 登录阶段：将验证码写入用户数据文件
    users = load_users()
    for username, user in users.items():
        if method == "email" and user.get("email") == contact:
            user.setdefault("verification_codes", {})[method] = {
                "code": code,
                "timestamp": timestamp
            }
            break
        elif method == "sms" and user.get("phone") == contact:
            user.setdefault("verification_codes", {})[method] = {
                "code": code,
                "timestamp": timestamp
            }
            break
    else:
        raise ValueError("未找到绑定该邮箱或手机号的用户")

    save_users(users)
    return True


def verify_code(input_code, stored_code_obj):
    """
    验证用户输入的验证码是否正确且未过期。
    """
    if not stored_code_obj:
        print("验证码对象不存在")
        return False

    stored_code = stored_code_obj.get("code")
    timestamp = stored_code_obj.get("timestamp")

    if not stored_code or not timestamp:
        print("验证码或时间戳缺失")
        return False

    if time.time() - timestamp > VERIFICATION_CODE_EXPIRY:
        print("验证码已过期")
        return False

    result = input_code == stored_code
    if not result:
        print("验证码不匹配")
    return result


def verify_first_factor(username, method, input_value):
    """
    验证第一因子（密码、短信验证码、邮箱验证码）。
    """
    user = get_user(username)
    if not user:
        return False

    if method == "password":
        return verify_password(user, input_value)

    stored = user.get("verification_codes", {}).get(method)
    return verify_code(input_value, stored)


def send_email_code(to_email, code):
    """
    发送邮件验证码（使用 QQ 邮箱 SMTP）。
    """
    # 构建邮件正文（纯文本）
    msg = MIMEText(f'您的 2FA 登录验证码：{code}', 'plain', 'utf-8')
    msg["Subject"] = Header("登录验证码", 'utf-8')
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email

    try:
        # 使用 SMTP SSL 发送邮件（端口 587 / 465）
        with smtplib.SMTP_SSL("smtp.qq.com", 587) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER, to_email, msg.as_string())

        print(f"[Email] 验证码发送成功：{to_email}")

    except Exception as e:
        # 特殊处理：会报错但邮件已成功发送（不知道为什么？？）
        if str(e) == "(-1, b'\\x00\\x00\\x00')":
            print("[Email] 虽然报错，但大概率已成功发送")
        else:
            print(f"[Email] 发送失败：{e}")
            raise


# 可替换为 alisms.py 中的 send_sms_code（阿里云）
def send_sms_code(to_phone, code):
    """
    使用 Twilio 发送短信验证码。
    """
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            body=f"您的验证码是: {code}",
            from_=TWILIO_PHONE,
            to=to_phone
        )
        print(f"[Twilio] 短信已发送：{message.sid}")
    except Exception as e:
        print(f"[Twilio] 发送失败：{e}")
        raise
