# gui_login.py

import tkinter as tk
from tkinter import messagebox

# 导入用户管理相关函数
from user_manager import (
    get_user,
    verify_recovery_code,
    get_remaining_attempts,
    is_user_locked,
    lock_user,
    reset_failed_attempts,
    increment_failed_attempts
)

# 导入验证码逻辑模块
from verification_manager import (
    send_code,
    verify_first_factor,
    verify_code as verify_input_code
)

# 登录界面模块（含第一因素认证）
class LoginViewMixin:
    def init_login(self):
        """
        构建登录界面，包括用户名、方式选择、验证码输入、按钮等
        """
        self.clear_window()

        # 页面标题
        tk.Label(self.root, text="登录", font=self.label_font_big).pack(pady=20, padx=10)

        # 用户名输入框
        tk.Label(self.root, text="用户名", font=self.label_font_mid).pack(pady=5, padx=10)
        username_entry = tk.Entry(self.root, font=self.entry_font, width=20)
        username_entry.pack(pady=5, padx=10)

        # 登录方式选择（密码、短信、邮箱）
        tk.Label(self.root, text="登录方式", font=self.label_font_mid).pack(pady=5)
        method_var = tk.StringVar(value="password")  # 默认使用密码登录
        method_menu = tk.OptionMenu(self.root, method_var, "password", "phone", "email")
        method_menu.config(font=self.label_font_mid, width=22)
        method_menu.pack(pady=5, padx=10)

        # 凭证输入框（密码或验证码）
        tk.Label(self.root, text="凭证（密码或验证码）", font=self.label_font_mid).pack(pady=5, padx=10)
        credential_entry = tk.Entry(self.root, show="*", font=self.entry_font, width=20)
        credential_entry.pack(pady=5, padx=10)

        # 发送验证码按钮（仅在选择短信/邮箱时启用）
        send_code_btn = tk.Button(
            self.root,
            text="发送验证码",
            **self.button_style,
            command=lambda: self.send_login_code(username_entry.get().strip(), method_var.get())
        )
        send_code_btn.pack(pady=5, padx=10)

        # 根据选择的方式启用/禁用验证码按钮
        def update_send_button(*args):
            method = method_var.get()
            send_code_btn.config(state="normal" if method in ("phone", "email") else "disabled")

        method_var.trace("w", update_send_button)
        update_send_button()

        # 登录按钮
        tk.Button(
            self.root,
            text="登录",
            command=lambda: self.login(username_entry, method_var, credential_entry),
            **self.button_style
        ).pack(pady=10)

        # 返回主菜单按钮
        tk.Button(self.root, text="返回", command=self.init_main_menu, **self.button_style).pack(pady=5)

    def send_login_code(self, username, method):
        """
        发送验证码（短信或邮箱）用于登录第一因子验证
        """
        try:
            send_code(username, method)  # 调用验证码模块
            messagebox.showinfo("成功", f"验证码已发送至 {method}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def login(self, username_entry, method_var, credential_entry):
        """
        登录逻辑处理，根据用户输入的方式与凭证进行验证
        """
        username = username_entry.get().strip()
        method = method_var.get()
        input_val = credential_entry.get().strip()

        # 获取用户信息
        user = get_user(username)
        if not user:
            messagebox.showerror("错误", "用户不存在")
            return

        # 判断账户是否被锁定
        if is_user_locked(user):
            messagebox.showerror("错误", "账户已被锁定，请稍后再试")
            return

        # 验证第一因子（密码、短信、邮箱）
        if method == "password":
            success = verify_first_factor(username, "password", input_val)
        else:
            stored = user.get("verification_codes", {}).get(method)
            success = verify_input_code(input_val, stored)

        # 登录成功
        if success:
            reset_failed_attempts(username)      # 重置失败次数
            self.username = username             # 保存当前登录用户
            self.init_totp_verification()        # 进入第二因子验证界面（TOTP）
        else:
            increment_failed_attempts(username)  # 增加失败次数
            remaining = get_remaining_attempts(username)
            if remaining <= 0:
                lock_user(username)
                messagebox.showerror("错误", "尝试次数过多，账户已锁定")
            else:
                messagebox.showerror("错误", f"验证失败，剩余尝试次数：{remaining}")
