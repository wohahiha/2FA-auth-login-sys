# alisms.py

# 阿里云 SDK 客户端及通用请求类
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

import json

# 替换为自己的阿里云 AccessKey 和短信签名/模板
ACCESS_KEY_ID = "AccessKeyId"
ACCESS_KEY_SECRET = "AccessKeySecret"
SIGN_NAME = "短信签名"
TEMPLATE_CODE = "模板CODE"

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
    request.set_method('POST')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    # 设置请求参数
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('PhoneNumbers', phone_number)
    request.add_query_param('SignName', SIGN_NAME)  # 签名名称（必须审核通过）
    request.add_query_param('TemplateCode', TEMPLATE_CODE)  # 模板 CODE（必须审核通过）

    # 设置模板参数（变量名必须与模板中定义的一致）
    request.add_query_param('TemplateParam', json.dumps({"code": code}))

    try:
        # 发送请求并获取响应
        response = client.do_action_with_exception(request)

        # 解析响应
        result = json.loads(response)

        # 判断是否发送成功
        if result.get("Code") == "OK":
            print(f"[AliSMS] 验证码发送成功：{phone_number}")
            return True
        else:
            print(f"[AliSMS] 发送失败：{result}")
            return False

    except Exception as e:
        print(f"[AliSMS] 异常：{e}")
        return False
