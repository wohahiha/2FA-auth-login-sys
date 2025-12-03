# gui_register.py


import tkinter as tk
from tkinter import messagebox

# 导入用户管理模块
from user_manager import add_user, get_user

# 导入 TOTP 管理模块
from totp_manager import generate_secret, generate_qr_code

# 导入验证码模块
from verification_manager import send_code, verify_code as verify_input_code


class RegisterViewMixin:
    """
    注册界面模块，包含注册页面、验证码验证、注册完成逻辑。
    """

    def init_register(self):
        """
        构建注册页面 UI，包含用户名、密码、手机号、邮箱等输入项。
        """
        self.clear_window()
        self.pending_user = {}  # 用于暂存注册数据

        # 页面标题
        tk.Label(self.root, text="注册新用户", width=17, font=self.label_font_big).pack(pady=10, padx=20)

        # 表单变量
        username_var = tk.StringVar()
        password1_var = tk.StringVar()
        password2_var = tk.StringVar()
        phone_var = tk.StringVar()
        email_var = tk.StringVar()

        # 用户名输入
        tk.Label(self.root, text="用户名 *", font=self.label_font_mid).pack(pady=5, padx=20)
        tk.Entry(self.root, textvariable=username_var, font=self.entry_font).pack(pady=5, padx=20)

        # 密码输入
        tk.Label(self.root, text="密码 *（至少8位）", font=self.label_font_mid).pack(pady=5, padx=20)
        tk.Entry(self.root, textvariable=password1_var, font=self.entry_font, show="*").pack(pady=5, padx=20)

        # 确认密码输入
        tk.Label(self.root, text="确认密码 *", font=self.label_font_mid).pack(pady=5, padx=20)
        tk.Entry(self.root, textvariable=password2_var, font=self.entry_font, show="*").pack(pady=5, padx=20)

        # 手机号输入（可选）
        tk.Label(self.root, text="手机号（可选）", font=self.label_font_mid).pack(pady=5, padx=20)
        tk.Label(self.root, text="国际格式，如 +8613812345678", font=self.label_font_small).pack(pady=5, padx=20)
        tk.Entry(self.root, textvariable=phone_var, font=self.entry_font).pack(pady=5, padx=20)

        # 邮箱输入（可选）
        tk.Label(self.root, text="邮箱（可选）", font=self.label_font_mid).pack()
        tk.Entry(self.root, textvariable=email_var, font=self.entry_font).pack()

        def start_verification():
            """
            开始注册前的验证逻辑，包括：
            - 表单校验
            - 用户名是否存在
            - 发送验证码（优先短信，其次邮箱）
            """
            username = username_var.get().strip()
            pw1 = password1_var.get()
            pw2 = password2_var.get()
            phone = phone_var.get().strip()
            email = email_var.get().strip()

            # 校验基本字段
            if not username or not pw1 or not pw2:
                messagebox.showerror("错误", "用户名和密码不能为空")
                return

            if len(pw1) < 8:
                messagebox.showerror("错误", "密码长度不能少于8位")
                return

            if pw1 != pw2:
                messagebox.showerror("错误", "两次密码不一致")
                return

            if get_user(username):
                messagebox.showerror("错误", "用户名已存在")
                return

            # 构建待注册用户数据
            self.pending_user = {
                "username": username,
                "password": pw1,
                "secret": generate_secret(),
                "phone": phone if phone else None,
                "email": email if email else None
            }

            # 手机号验证
            if phone:
                try:
                    result = send_code(phone, "sms", is_registration=True)
                    self.pending_user["sms_code"] = result["code"]
                    self.pending_user["sms_timestamp"] = result["timestamp"]
                    self.verify_code_ui("sms", phone)
                    return
                except Exception as e:
                    messagebox.showerror("错误", f"短信发送失败：{e}")
                    return

            # 邮箱验证
            if email:
                try:
                    result = send_code(email, "email", is_registration=True)
                    self.pending_user["email_code"] = result["code"]
                    self.pending_user["email_timestamp"] = result["timestamp"]
                    self.verify_code_ui("email", email)
                    return
                except Exception as e:
                    messagebox.showerror("错误", f"邮件发送失败：{e}")
                    return

            # 如果都没有填写，直接完成注册
            self.finalize_registration()

        # 提示信息
        tk.Label(
            self.root,
            text="未填写邮箱/电话将无法使用对应方式找回账户",
            font=self.label_font_small
        ).pack(pady=5)

        # 提交按钮
        tk.Button(
            self.root, text="提交注册", command=start_verification, **self.button_style
        ).pack(pady=10)

        # 返回按钮
        tk.Button(
            self.root, text="返回", command=self.init_main_menu, **self.button_style
        ).pack(pady=5)

    def verify_code_ui(self, method, contact):
        """
        构建验证码输入界面，用于验证短信或邮箱验证码。
        """
        self.clear_window()
        tk.Label(self.root, text=f"请输入发送到 {contact} 的验证码", font=self.label_font_mid).pack(pady=10)
        code_var = tk.StringVar()
        tk.Entry(self.root, textvariable=code_var, font=self.entry_font).pack()

        def verify_and_continue():
            """
            验证用户输入的验证码是否正确。
            - 如果是短信验证成功，则继续验证邮箱；
            - 如果是邮箱验证成功，则完成注册。
            """
            input_code = code_var.get().strip()
            stored_code = {
                "code": self.pending_user.get(f"{method}_code"),
                "timestamp": self.pending_user.get(f"{method}_timestamp")
            }

            if verify_input_code(input_code, stored_code):
                if method == "sms" and self.pending_user.get("email"):
                    try:
                        result = send_code(self.pending_user["email"], "email", is_registration=True)
                        self.pending_user["email_code"] = result["code"]
                        self.pending_user["email_timestamp"] = result["timestamp"]
                        self.verify_code_ui("email", self.pending_user["email"])
                        return
                    except Exception as e:
                        messagebox.showerror("错误", f"邮件发送失败：{e}")
                        return
                else:
                    self.finalize_registration()
            else:
                messagebox.showerror("错误", "验证码错误或已过期")

        # 确认按钮
        tk.Button(self.root, text="确认", command=verify_and_continue, **self.button_style).pack(pady=10)

    def finalize_registration(self):
        """
        注册完成逻辑：
        - 保存用户信息
        - 显示二维码
        - 显示恢复码
        """
        try:
            add_user(
                self.pending_user["username"],
                self.pending_user["secret"],
                self.pending_user["password"],
                email=self.pending_user.get("email"),
                phone=self.pending_user.get("phone")
            )
        except Exception as e:
            messagebox.showerror("错误", str(e))
            return

        self.clear_window()

        username = self.pending_user["username"]
        secret = self.pending_user["secret"]

        # 显示二维码提示
        tk.Label(
            self.root,
            text="请使用 Authenticator 应用扫描以下二维码",
            font=self.label_font_mid
        ).pack(pady=10)

        # 弹出二维码图像窗口
        generate_qr_code(username, secret)

        # 获取恢复码
        user = get_user(username)
        recovery_codes = user.get("recovery_codes", [])

        # 显示恢复码（可复制）
        tk.Label(
            self.root,
            text="请妥善保存以下恢复码（每个码只能使用一次）：",
            font=self.label_font_mid
        ).pack(pady=10)

        for code in recovery_codes:
            entry = tk.Entry(self.root, font=self.entry_font, justify="center")
            entry.insert(0, code)
            entry.config(state="readonly")
            entry.pack(pady=2)

        # 返回登录按钮
        tk.Button(
            self.root,
            text="返回登录",
            command=self.init_main_menu,
            **self.button_style
        ).pack(pady=20)
