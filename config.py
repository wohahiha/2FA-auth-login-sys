# config.py

from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv()

# 验证码有效期（秒）
VERIFICATION_CODE_EXPIRY = 300

# 日志文件路径
LOG_FILE = "login_logs.json"

# 邮件配置（替换为自己的相关信息）
EMAIL_SENDER = "邮箱"
EMAIL_PASSWORD = "授权码/应用码"

# Twilio 配置（替换为自己的相关信息）
TWILIO_SID = "twilio-sid"
TWILIO_TOKEN = "twilio-token"
TWILIO_PHONE = "twilio-phone"

# # 加密密钥
# FERNET_KEY = os.getenv("FERNET_KEY")
# if not FERNET_KEY:
#     raise ValueError("未设置 FERNET_KEY")

# 用户数据文件路径
USER_DATA_FILE = "users.json"

# 登录尝试限制
MAX_FAILED_ATTEMPTS = 5         # 最大失败次数
LOCK_DURATION = 300             # 锁定时间（秒）
