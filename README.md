# 2FA-auth-login-sys

一个基于 Python Tkinter 的双因素认证注册登录系统示例。项目实现了基础账户注册、密码登录、邮箱/短信验证码登录、TOTP 二次验证、恢复码、失败次数限制和账户临时锁定，适合学习 2FA 登录流程、TOTP 密钥管理和本地 JSON 数据存储。

## 功能特性

- 图形化注册与登录界面，入口文件为 `main.py`。
- 支持用户名、密码、手机号、邮箱注册。
- 支持密码、手机号验证码、邮箱验证码作为第一因素认证方式。
- 支持基于 Authenticator 应用的 TOTP 二次验证。
- 注册后生成二维码和一次性恢复码，恢复码可用于无法获取 TOTP 时登录。
- 使用 Fernet 对 TOTP 密钥进行对称加密后保存。
- 使用 SHA-256 保存密码摘要。
- 记录登录尝试日志，并在失败次数过多时临时锁定账户。
- 本地使用 `users.json` 保存用户数据，使用 `login_logs.json` 保存登录日志。

## 技术栈

- Python 3.12 及以下版本
- Tkinter
- python-dotenv
- cryptography / Fernet
- pyotp
- qrcode
- smtplib
- Twilio SDK
- Alibaba Cloud SMS SDK

## 安装与运行

建议使用 Python 3.12 或更低版本。Python 3.13 可能出现 Tkinter/Tcl 运行环境缺失问题。

```powershell
cd D:\Github\2FA
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install python-dotenv cryptography pyotp 'qrcode[pil]' twilio aliyun-python-sdk-core
python main.py
```

如果不使用虚拟环境，也可以在项目目录下直接安装依赖后运行：

```powershell
pip install python-dotenv cryptography pyotp 'qrcode[pil]' twilio aliyun-python-sdk-core
python main.py
```

## 环境变量配置

项目启动时会从 `.env` 读取 `FERNET_KEY`。如果没有配置该变量，`crypto_utils.py` 会抛出 `ValueError: 未设置 FERNET_KEY`。

生成 Fernet 密钥：

```powershell
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

在项目根目录创建 `.env`，写入：

```env
FERNET_KEY=<your-generated-fernet-key>
```

`.env` 中不要写入真实账号密码后提交到 GitHub。当前 `.gitignore` 已忽略 `.env`。

## 邮箱与短信配置

邮箱验证码使用 `verification_manager.py` 中的 `send_email_code`，配置项位于 `config.py`：

```python
EMAIL_SENDER = "邮箱"
EMAIL_PASSWORD = "授权码/应用码"
```

Twilio 短信验证码使用 `verification_manager.py` 中的 `send_sms_code`，配置项位于 `config.py`：

```python
TWILIO_SID = "twilio-sid"
TWILIO_TOKEN = "twilio-token"
TWILIO_PHONE = "twilio-phone"
```

阿里云短信示例位于 `alisms.py`，其中的 `ACCESS_KEY_ID`、`ACCESS_KEY_SECRET`、短信签名和模板参数都是占位符。实际使用时请改为环境变量或其他安全配置方式，不要把真实密钥提交到仓库。

## 使用流程

1. 运行 `python main.py` 打开主界面。
2. 点击注册，填写用户名和至少 8 位密码。
3. 可选填写手机号和邮箱；填写后会先完成对应验证码校验。
4. 注册完成后，使用 Authenticator 应用扫描二维码，并保存页面显示的一次性恢复码。
5. 返回登录页，选择密码、手机号或邮箱作为第一因素认证方式。
6. 第一因素通过后，输入 Authenticator 中的 TOTP 验证码，或输入未使用过的恢复码。
7. 如果连续验证失败超过限制，账户会被临时锁定。

## 项目结构

```text
2FA/
├── main.py                  # 程序入口
├── gui.py                   # 主界面与页面切换
├── gui_register.py          # 注册界面与注册验证码流程
├── gui_login.py             # 登录界面与第一因素认证
├── gui_totp.py              # TOTP / 恢复码二次验证界面
├── user_manager.py          # 用户创建、密码校验、恢复码和锁定逻辑
├── verification_manager.py  # 邮箱和短信验证码逻辑
├── totp_manager.py          # TOTP 密钥、二维码和验证码校验
├── crypto_utils.py          # Fernet 加密工具
├── data_store.py            # users.json 读写
├── logger.py                # 登录日志读写
├── config.py                # 配置项
├── alisms.py                # 阿里云短信示例
├── 1.png                    # 界面截图
├── 2.png
├── 3.png
└── 4.png
```

## 运行时文件

程序运行后可能生成以下本地文件：

- `users.json`：用户数据、加密后的 TOTP 密钥、恢复码、失败次数等。
- `login_logs.json`：登录尝试日志。
- `.env`：本地环境变量文件。

这些文件可能包含敏感信息或本地状态，不建议提交到公开仓库。

## 常见问题

### Python 3.13 Tkinter 报错

如果使用的 Python 版本大于 3.12，可能出现类似报错：

```text
_tkinter.TclError: Can't find a usable init.tcl in the following directories:
D:/python3.13/lib/tcl8.6 D:/py_ff/.venv/lib/tcl8.6 D:/py_ff/lib/tcl8.6 D:/py_ff/.venv/library D:/py_ff/library D:/py_ff/tcl8.6.14/library D:/tcl8.6.14/library

This probably means that Tcl wasn't installed properly.
```

可选解决方式：

1. 使用 Python 3.12 或更低版本。
2. 重新安装包含 Tk/Tcl 的 Python 发行版。
3. 将缺失的 `init.tcl` 放入报错提示中提到的任一目录。

### 启动时报 `未设置 FERNET_KEY`

请先按“环境变量配置”章节生成 Fernet 密钥，并在 `.env` 中写入 `FERNET_KEY`。

### 收不到邮箱或短信验证码

请确认邮箱授权码、SMTP 登录配置、Twilio 配置或阿里云短信配置已替换为自己的有效配置，并确认网络和服务商侧权限正常。

## 安全说明

本项目主要用于学习和演示双因素认证流程。当前实现仍是教学示例，不建议不经改造直接用于生产环境。生产环境中应至少补充更强的密码哈希方案、数据库存储、密钥轮换、审计日志、异常处理、速率限制、服务端会话管理和完整测试。

不要提交 `.env`、真实邮箱授权码、短信服务 token、AccessKey、用户数据文件或日志文件。

## 界面展示

![](./1.png)

![](./2.png)

![](./3.png)

![](./4.png)

## 许可证

本项目基于 MIT License 开源，详见 [LICENSE](./LICENSE)。
