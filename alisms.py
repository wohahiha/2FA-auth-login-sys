# alisms.py

# 阿里云 SDK 客户端及通用请求类
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json  # 用于构造请求参数和解析响应

# ✅ 替换为你在阿里云控制台中申请的 AccessKey 和短信签名/模板
ACCESS_KEY_ID = "你的AccessKeyId"  # 阿里云账号的 AccessKey ID
ACCESS_KEY_SECRET = "你的AccessKeySecret"  # 阿里云账号的 AccessKey Secret
SIGN_NAME = "你的短信签名"  # 例如："某某科技"
TEMPLATE_CODE = "你的模板CODE"  # 例如："SMS_123456789"

# 创建阿里云短信客户端（指定区域为 cn-hangzhou）
client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, "cn-hangzhou")


def send_sms_code(phone_number, code):
    """
    发送短信验证码到指定手机号（使用阿里云短信服务）。

    参数:
        phone_number (str): 接收短信的手机号（必须为中国大陆号码，格式如 "+8613812345678" 或 "13812345678"）
        code (str): 要发送的验证码（通常为 6 位数字）

    返回:
        bool: 发送是否成功（True 表示成功，False 表示失败）
    """

    # 创建通用请求对象
    request = CommonRequest()
    request.set_method('POST')  # 请求方式：POST
    request.set_domain('dysmsapi.aliyuncs.com')  # 阿里云短信服务域名
    request.set_version('2017-05-25')  # API 版本
    request.set_action_name('SendSms')  # 动作名称：发送短信

    # 设置请求参数
    request.add_query_param('RegionId', 'cn-hangzhou')  # 区域 ID
    request.add_query_param('PhoneNumbers', phone_number)  # 接收短信的手机号
    request.add_query_param('SignName', SIGN_NAME)  # 签名名称（必须审核通过）
    request.add_query_param('TemplateCode', TEMPLATE_CODE)  # 模板 CODE（必须审核通过）

    # 设置模板参数（变量名必须与模板中定义的一致）
    request.add_query_param('TemplateParam', json.dumps({"code": code}))

    try:
        # 发送请求并获取响应（可能抛出异常）
        response = client.do_action_with_exception(request)

        # 解析响应为 Python 字典
        result = json.loads(response)

        # 判断是否发送成功（Code == "OK" 表示成功）
        if result.get("Code") == "OK":
            print(f"[AliSMS] 验证码发送成功：{phone_number}")
            return True
        else:
            # 打印失败原因（如签名未审核、模板不匹配等）
            print(f"[AliSMS] 发送失败：{result}")
            return False

    except Exception as e:
        # 捕获并打印异常（如网络问题、身份验证失败等）
        print(f"[AliSMS] 异常：{e}")
        return False
