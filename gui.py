# gui.py

import tkinter as tk

# 导入功能模块（注册界面、登录界面、TOTP 验证界面）
from gui_register import RegisterViewMixin
from gui_login import LoginViewMixin
from gui_totp import TOTPViewMixin

# 主 GUI 类，继承三个功能模块
class TwoFAGUI(RegisterViewMixin, LoginViewMixin, TOTPViewMixin):
    def __init__(self, root):
        """
        初始化主界面窗口，设置样式、状态变量、默认页面等
        """
        super().__init__()

        # Tkinter 根窗口
        self.root = root
        self.root.title("2FA 验证系统")  # 设置窗口标题
        self.root.configure(bg="#f9f9f9")  # 设置背景颜色

        # 设置窗口大小
        # self.root.geometry("600x500")

        # 注册阶段使用的用户缓存数据（未提交前）
        self.pending_user = None  # 用于暂存注册信息
        self.username = ""        # 当前登录用户的用户名

        # Label 样式配置
        self.label_font_big = ("SimSun", 30)
        self.label_font_mid = ("SimSun", 16)
        self.label_font_small = ("SimSun", 10)

        # Entry 样式配置
        self.entry_font = ("SimSun", 20)

        # Bttton 样式配置
        self.button_style = {
            "font": ("SimSun", 16),              # 字体
            "bg": "#95c0c7",                     # 背景色（按钮默认色）
            "fg": "#470024",                     # 文字颜色
            "activebackground": "#ba5fb6",       # 鼠标悬停背景色
            "width": 20,                         # 宽度（字符数）
            "padx": 5,                           # 内边距 X
            "pady": 5,                           # 内边距 Y
            "bd": 0                              # 边框宽度
        }

        # 初始化首页（主菜单）
        self.init_main_menu()

    def clear_window(self):
        """
        清空当前窗口中的所有控件（用于页面切换）
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def init_main_menu(self):
        """
        主菜单页面：展示欢迎信息与入口按钮（注册、登录）
        """
        self.clear_window()

        # 欢迎标题
        tk.Label(
            self.root,
            text="欢迎使用 2FA 系统",
            font=self.label_font_big
        ).pack(pady=20, padx=20)

        # 注册按钮，跳转注册界面
        tk.Button(
            self.root,
            text="注册",
            command=self.init_register,  # RegisterViewMixin
            **self.button_style
        ).pack(pady=10)

        # 登录按钮，跳转登录界面
        tk.Button(
            self.root,
            text="登录",
            command=self.init_login,  # LoginViewMixin
            **self.button_style
        ).pack(pady=10)
