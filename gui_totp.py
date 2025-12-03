# gui_totp.py


import tkinter as tk
from tkinter import messagebox

# 导入 TOTP 验证函数
from totp_manager import verify_totp

# 导入用户管理函数
from user_manager import (
    verify_recovery_code,
    increment_failed_attempts,
    get_remaining_attempts,
    lock_user
)

class TOTPViewMixin:
    """
    TOTP 验证界面模块，用于第二因子验证（基于 TOTP 或恢复码）。
    """
    def init_totp_verification(self):
        """
        构建 TOTP 验证界面，供用户输入 TOTP 或恢复码。
        """
        self.clear_window()

        # 页面标题
        tk.Label(
            self.root,
            text="请输入 TOTP 验证码或恢复码",
            font=self.label_font_mid
        ).pack(pady=10)

        # TOTP 输入框
        code_entry = tk.Entry(self.root, font=self.entry_font)
        code_entry.pack()

        def verify_totp_code():
            """
            验证用户输入的 TOTP 或恢复码是否正确。
            如果正确，则登录成功；
            如果错误，则增加失败次数，并根据剩余次数提示或锁定账户。
            """
            code = code_entry.get().strip()

            # 尝试验证 TOTP 或恢复码
            if verify_totp(self.username, code) or verify_recovery_code(self.username, code):
                messagebox.showinfo("登录成功", f"欢迎回来，{self.username}！")
                self.init_main_menu()  # 返回主菜单
            else:
                # 验证失败，增加失败次数
                increment_failed_attempts(self.username)
                remaining = get_remaining_attempts(self.username)

                if remaining <= 0:
                    lock_user(self.username)
                    messagebox.showerror("错误", "尝试次数过多，账户已锁定")
                else:
                    messagebox.showerror("错误", f"验证码错误，剩余尝试次数：{remaining}")

        # 确认按钮
        tk.Button(
            self.root,
            text="确认",
            command=verify_totp_code,
            **self.button_style
        ).pack(pady=10)
