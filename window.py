import tkinter as tk
from tkinter import ttk
import s_des


class Entry:
    def __init__(self):
        self.entry_1 = tk.Entry
        self.entry_2 = tk.Entry
        self.entry_3 = tk.Entry
        self.sdes = s_des.SimpleDes()

    def on_button_click(self, leaf):
        # 在按钮点击时执行的函数
        entry1_value = self.entry_1.get()
        entry2_value = self.entry_2.get()

        if leaf == 1:
            result = self.sdes.set_key_b(entry2_value)
            if result == "密钥设置成功":
                if entry1_value.startswith("0b"):
                    result = self.sdes.encrypt_b(entry1_value)
                else:
                    if entry1_value.isascii():
                        result = self.sdes.encrypt_a(entry1_value)
                    else:
                        result = "明文包含错误字符"

            self.entry_3.config(state="normal")
            self.entry_3.delete(0, tk.END)
            self.entry_3.insert(0, result)
            self.entry_3.config(state="readonly")

        elif leaf == 2:
            result = self.sdes.set_key_b(entry2_value)
            if result == "密钥设置成功":
                if entry1_value.startswith("0b"):
                    result = self.sdes.decrypt_b(entry1_value)
                else:
                    result = self.sdes.decrypt_a(entry1_value)

            self.entry_3.config(state="normal")
            self.entry_3.delete(0, tk.END)
            self.entry_3.insert(0, result)
            self.entry_3.config(state="readonly")

        elif leaf == 3:
            if entry1_value.startswith("0b") & entry2_value.startswith("0b"):
                result, times = self.sdes.crack_b(entry1_value, entry2_value)
            else:
                if len(entry1_value) == len(entry2_value):
                    result, times = self.sdes.crack_a(entry1_value, entry2_value)
                else:
                    result = "明密文不对应"

            self.entry_3.config(state="normal")
            self.entry_3.delete(0, tk.END)
            self.entry_3.insert(0, result)
            self.entry_3.config(state="readonly")

        elif leaf == 4:
            if entry1_value.startswith("0b") & entry2_value.startswith("0b"):
                keys, result = self.sdes.crack_b(entry1_value, entry2_value)
            else:
                if len(entry1_value) == len(entry2_value):
                    keys, result = self.sdes.crack_a(entry1_value, entry2_value)
                else:
                    result = "明密文不对应"

            self.entry_3.config(state="normal")
            self.entry_3.delete(0, tk.END)
            self.entry_3.insert(0, result)
            self.entry_3.config(state="readonly")


class Window:
    def main(self):
        # 创建主窗口
        root = tk.Tk()
        root.title("S-DES")
        root.geometry("400x300+560+280")

        # 创建分页标签控件
        notebook = ttk.Notebook(root)

        # 创建第一个选项卡
        tab_1 = ttk.Frame(notebook)
        notebook.add(tab_1, text="加密")

        # 创建第二个选项卡
        tab_2 = ttk.Frame(notebook)
        notebook.add(tab_2, text="解密")

        tab_3 = ttk.Frame(notebook)
        notebook.add(tab_3, text="破解")

        tab_4 = ttk.Frame(notebook)
        notebook.add(tab_4, text="碰撞")

        # 将 ttk.Notebook 放置在主窗口中
        notebook.pack()

        self.page(tab_1, 1)
        self.page(tab_2, 2)
        self.page(tab_3, 3)
        self.page(tab_4, 4)

        # 放大 ttk.Notebook 以适应窗口大小
        notebook.pack(fill=tk.BOTH, expand=True)

        # 启动主循环
        root.mainloop()

    @staticmethod
    def page(root, leaf):
        entry = Entry()

        # 设置行和列的权重
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # 创建 ttk.Frame 实例
        frame = ttk.Frame(root)
        frame.grid(row=0, column=0, padx=10, pady=10)

        # 创建输入框
        label_1 = tk.Label(frame, text="账户:")
        label_1.grid(row=0, column=0, padx=20, pady=10, )
        entry.entry_1 = ttk.Entry(frame)
        entry.entry_1.grid(row=0, column=1, padx=20, pady=10)

        label_2 = tk.Label(frame, text="账户:")
        label_2.grid(row=1, column=0, padx=20, pady=10)
        entry.entry_2 = ttk.Entry(frame)
        entry.entry_2.grid(row=1, column=1, padx=20, pady=10)

        label_3 = tk.Label(frame, text="账户:")
        label_3.grid(row=2, column=0, padx=20, pady=10)
        entry.entry_3 = ttk.Entry(frame, state="readonly")
        entry.entry_3.grid(row=2, column=1, padx=20, pady=10)

        # 创建按钮
        button = ttk.Button(root)
        button.grid(row=1, column=0, padx=10, pady=10)

        if leaf == 1:
            label_1.config(text="明文")
            label_2.config(text="密钥")
            label_3.config(text="密文")
            button.config(text="加密", command=lambda: entry.on_button_click(leaf))
        elif leaf == 2:
            label_1.config(text="密文")
            label_2.config(text="密钥")
            label_3.config(text="明文")
            button.config(text="解密", command=lambda: entry.on_button_click(leaf))
        elif leaf == 3:
            label_1.config(text="明文")
            label_2.config(text="密文")
            label_3.config(text="密钥")
            button.config(text="破解", command=lambda: entry.on_button_click(leaf))
        elif leaf == 4:
            label_1.config(text="明文")
            label_2.config(text="密文")
            label_3.config(text="次数")
            button.config(text="碰撞", command=lambda: entry.on_button_click(leaf))
