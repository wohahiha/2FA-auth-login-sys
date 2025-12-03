# config.py

from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv()


def _required_env(name: str, cast=None):
    """
    获取必需的环境变量，必要时进行类型转换；若缺失或格式错误则抛出异常。
    """
    value = os.getenv(name)
    if value is None or value == "":
        raise ValueError(f"未设置 {name}")
    if cast:
        try:
            return cast(value)
        except Exception as exc:  # 转换失败时给出明确提示
            raise ValueError(f"{name} 格式错误: {exc}") from exc
    return value


# 验证码有效期（秒）
VERIFICATION_CODE_EXPIRY = _required_env("VERIFICATION_CODE_EXPIRY", int)

# 日志文件路径
LOG_FILE = _required_env("LOG_FILE")

# 邮件配置
EMAIL_SENDER = _required_env("EMAIL_SENDER")
EMAIL_PASSWORD = _required_env("EMAIL_PASSWORD")

# Twilio 配置
TWILIO_SID = _required_env("TWILIO_SID")
TWILIO_TOKEN = _required_env("TWILIO_TOKEN")
TWILIO_PHONE = _required_env("TWILIO_PHONE")

# 加密密钥（供 crypto_utils 使用）
FERNET_KEY = _required_env("FERNET_KEY")

# 用户数据文件路径
USER_DATA_FILE = _required_env("USER_DATA_FILE")

# 登录尝试限制
MAX_FAILED_ATTEMPTS = _required_env("MAX_FAILED_ATTEMPTS", int)  # 最大失败次数
LOCK_DURATION = _required_env("LOCK_DURATION", int)              # 锁定时间（秒）
