import os
import re
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime

COPYRIGHT = "© 灯火通明（济宁）网络有限公司"

def is_mafile(filename):
    return filename.endswith('.maFile') or filename.endswith('.json')

def parse_accounts(input_str):
    """
    支持多行格式，分隔符可为:、--、----，或只写账号
    """
    accounts = set()
    lines = input_str.strip().splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        for sep in ['----', '--', ':']:
            if sep in line:
                account = line.split(sep, 1)[0].strip()
                break
        else:
            account = line  # 没有分隔符，整行就是账号
        if account:
            accounts.add(account)
    return accounts

def filter_mafiles_by_account(src_dir, accounts, output_func):
    matched_files = []
    failed_files = 0
    matched_accounts = set()
    already_matched = set()
    # 只允许“纯账号名.扩展名”格式，不允许带括号(1)等
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if is_mafile(file):
                # 正则匹配标准账号文件名（不含括号）
                m = re.match(r"^([a-zA-Z0-9]+)\.(maFile|json)$", file)
                if not m:
                    continue  # 跳过带(1)等变体的
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    acc_name = str(data.get('account_name', '')).strip()
                    if acc_name in accounts and acc_name not in already_matched:
                        matched_files.append((filepath, file))
                        matched_accounts.add(acc_name)
                        already_matched.add(acc_name)
                        output_func(f"[√] 匹配成功: {file}\n")
                except Exception as e:
                    failed_files += 1
                    output_func(f"[!] 跳过无法解析的文件: {file} 错误: {e}\n")
    return matched_files, failed_files, matched_accounts

class MafileSelectorApp:
    def __init__(self, master):
        self.master = master
        master.title("maFile批量筛选工具 - 灯火通明")
        master.geometry("900x670")
        master.resizable(False, False)
        self.src_dir = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill="both", expand=True)

        # 路径选择区
        path_frame = tk.LabelFrame(main_frame, text="maFile目录选择", padx=10, pady=8)
        path_frame.pack(fill="x", padx=16, pady=8)
        tk.Label(path_frame, text="maFile目录:").pack(side="left")
        self.dir_entry = tk.Entry(path_frame, textvariable=self.src_dir, width=60)
        self.dir_entry.pack(side="left", padx=5)
        tk.Button(path_frame, text="浏览", command=self.browse_src).pack(side="left", padx=4)
        tk.Button(path_frame, text="打开", command=self.open_dir).pack(side="left")

        # 账号输入区
        input_frame = tk.LabelFrame(main_frame, text="账号列表输入", padx=10, pady=8)
        input_frame.pack(fill="x", padx=16, pady=4)
        tk.Label(input_frame, text="每行账号:密码，账号--密码，账号----密码或账号：").pack(anchor="w")
        self.accounts_text = scrolledtext.ScrolledText(input_frame, width=90, height=9, font=("Consolas", 11))
        self.accounts_text.pack(fill="x", pady=(2,0))
        tk.Label(input_frame, text="可直接粘贴站点点导出的账号列表", fg="gray").pack(anchor="w", pady=(2,0))

        # 操作区
        op_frame = tk.Frame(main_frame)
        op_frame.pack(pady=18)
        self.start_btn = tk.Button(
            op_frame, text="筛选复制", command=self.filter_files,
            bg="#4caf50", fg="white", width=18, height=2,
            font=("微软雅黑", 13, "bold")
        )
        self.start_btn.pack()

        # 输出区
        output_frame = tk.LabelFrame(main_frame, text="运行日志", padx=10, pady=8)
        output_frame.pack(fill="both", padx=16, pady=6, expand=True)
        self.output_text = scrolledtext.ScrolledText(output_frame, width=100, height=10, font=("Consolas", 11))
        self.output_text.pack(fill="both", expand=True)

        # 版权信息
        copyright_frame = tk.Frame(self.master)
        copyright_frame.place(relx=0, rely=1, anchor='sw', relwidth=1)
        copyright_label = tk.Label(
            copyright_frame,
            text=COPYRIGHT,
            anchor="e",
            fg="gray",
            font=("微软雅黑", 10)
        )
        copyright_label.pack(side="right", padx=10, pady=4, anchor="e")

    def browse_src(self):
        directory = filedialog.askdirectory(title="选择maFile目录")
        if directory:
            self.src_dir.set(directory)

    def open_dir(self):
        path = self.src_dir.get()
        if os.path.isdir(path):
            os.startfile(path)
        else:
            messagebox.showwarning("提示", "请选择正确的maFile目录")

    def filter_files(self):
        src = self.src_dir.get()
        accounts_str = self.accounts_text.get("1.0", tk.END)
        if not src or not os.path.isdir(src):
            messagebox.showwarning("提示", "请先选择正确的maFile目录！")
            return
        accounts = parse_accounts(accounts_str)
        if not accounts:
            messagebox.showwarning("提示", "请输入账号！")
            return

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert("end", f"开始筛选，账号集合：{accounts}\n\n")

        def output_func(msg):
            self.output_text.insert("end", msg)
            self.output_text.see("end")

        matched_files, failed_files, matched_accounts = filter_mafiles_by_account(src, accounts, output_func)

        # 输出未匹配账号列表
        unmatched_accounts = accounts - matched_accounts
        if unmatched_accounts:
            self.output_text.insert("end", "\n未匹配成功的账号列表：\n")
            for acc in sorted(unmatched_accounts):
                self.output_text.insert("end", f"  {acc}\n")
            self.output_text.insert("end", "\n未匹配成功的账号可能原因：\n")
            self.output_text.insert("end", "1. 该账号没有对应的maFile文件；\n")
            self.output_text.insert("end", "2. maFile文件损坏或无法解析；\n")
            self.output_text.insert("end", "3. 账号字段填写有误。\n")

        if not matched_files:
            self.output_text.insert("end", "\n未找到匹配的maFile文件。\n")
            msg = "未找到匹配的maFile文件。"
            if failed_files > 0:
                msg += f"\n并有 {failed_files} 个文件解析失败，详情请见日志。"
            messagebox.showinfo("结果", msg)
            return

        nowstr = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst_dir = os.path.join(os.path.dirname(src), f"maFile{nowstr}")
        os.makedirs(dst_dir, exist_ok=True)

        for src_filepath, filename in matched_files:
            dst_filepath = os.path.join(dst_dir, filename)
            shutil.copyfile(src_filepath, dst_filepath)
            display_path = dst_filepath.replace('\\', '/')
            self.output_text.insert("end", f"[+] 已复制到: {display_path}\n")

        dst_display = dst_dir.replace('\\', '/')
        self.output_text.insert("end", f"\n筛选完成，共复制 {len(matched_files)} 个maFile文件到 {dst_display}\n")
        msg = f"筛选完成，共复制 {len(matched_files)} 个maFile文件到:\n{dst_display}"
        if failed_files > 0:
            msg += f"\n\n有 {failed_files} 个文件解析失败，详情请见日志。"
        if messagebox.askyesno("完成", msg + "\n\n是否打开目标文件夹？"):
            os.startfile(dst_dir)

if __name__ == '__main__':
    root = tk.Tk()
    app = MafileSelectorApp(root)
    root.mainloop()