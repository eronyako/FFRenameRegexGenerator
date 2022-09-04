#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Subj: PyCharm
# @File: FFRenameRegexGeneratorGUI.py
# @Date: 2022/9/3 22:53

import tkinter as tk
import tkinter.messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
import os


# 定义转换函数
def regex_convert(regex_list):
    """
    此函数用于正则表达式转换
    :param regex_list: 正则表达式文件内容，str
    :return: 批处理命令文件内容,str
    """
    # 去除换行符
    i = 0
    for v in regex_list:
        regex_list[i] = v.strip()
        i += 1

    regex = []
    i = 0
    verify = False
    for v in regex_list:
        if v == '':
            continue
        elif v[0] == '#':
            continue
        elif v[0] == '(':
            if not verify:
                regex.append([])
                regex[i].append(v)
                verify = True
            else:
                raise ValueError('不是有效的正则式列表')
        else:
            if verify:
                regex[i].append(v)
                i += 1
                verify = False
            else:
                raise ValueError('不是有效的正则式列表')

    # 生成 FFRename Pro 的正则表达式 frc 文件

    date0 = 'CMD_A120220816'
    date1 = 103514300

    file0 = """;===========================================================
;批处理命令文件
;菲菲更名宝贝 之 得意非凡 (FFRename Professional)
;菲菲的家(ffhome.com)版权所有
;
;说明：本文件为系统生成，除非明白各参数之意义，否则请不要随
;      意改动，以免影响原有的更名结果！
;===========================================================
"""

    file1 = '[CommandList]\nCommandListCount=' + str(len(regex)) + '\n'
    cmd_list = []
    i = 1
    while i <= len(regex):
        cmd_list.append(date0 + str(date1))
        file1 = file1 + str(i) + '=' + date0 + str(date1) + '\n'
        i += 1
        date1 += 1000

    i = 0
    file2 = ''
    for v in cmd_list:
        file2 = file2 + '\n[' + v + ']\nCMDComment=正则表达式更名\nCMDid=A101\nA1_Regex=1\nA1_RegexText=|'
        file2 = file2 + regex[i][0] + '|\nA1_RegexReplaceText=|' + regex[i][1]
        file2 = file2 + '|\nA1_RegexIncludeExt=0\nA1_RegexReplaceAll=0\nA1_RegexReplaceSome=0\n' \
                        'A1_RegexReplaceSomeText=1\nA1_RegexReplaceSomeGetOnly=1\n' \
                        'A1_RegexReplaceSomeGetOnlyText=1\n'
        i += 1

    file = file0 + file1 + file2
    return file


# 定义主页面
class Application(ttk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, padding=10, **kwargs)
        self.var_output_name = None
        self.var_input_file = None
        self.var_input_content = []
        self.var_output_content = []
        self.pack()

        self.frame = ttk.Frame()
        self.frame.pack(side=TOP, fill=BOTH, expand=YES)

        # 定义框架
        self.frame_in = ttk.Frame(self.frame)
        self.frame_in.grid_rowconfigure(1, weight=1)
        self.frame_in.grid_columnconfigure(1, weight=1)
        self.frame_in.pack(side=LEFT, fill=BOTH, expand=YES)

        self.frame_out = ttk.Frame(self.frame)
        self.frame_out.grid_rowconfigure(1, weight=1)
        self.frame_out.grid_columnconfigure(0, weight=1)
        self.frame_out.pack(side=LEFT, fill=BOTH, expand=YES)

        # 输入区
        self.select_file_btn = ttk.Button(self.frame_in, text='选择文件', command=self.select_file,
                                          bootstyle='primary_outline')
        self.input_file_name = ttk.Entry(self.frame_in)

        self.input_txt = ttk.Text(self.frame_in)
        self.input_txt.insert(END, '请选择正则表达式文件')

        # 输出区
        self.output_file_name = ttk.Entry(self.frame_out)
        self.save_file_btn = ttk.Button(self.frame_out, text='保存文件', command=self.save_file)

        self.output_txt = ttk.Text(self.frame_out)
        self.output_txt.insert(END, 'FFRename frc 文件预览区')

        # 生成页面
        self.create_widget()

    def create_widget(self):
        # 输入区
        self.select_file_btn.grid(row=0, column=0, padx=10, pady=5)
        self.input_file_name.grid(row=0, column=1, padx=10, pady=5, sticky=W + E)
        self.input_txt.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=W + N + E + S)

        # 输出区
        self.output_file_name.grid(row=0, column=0, padx=10, pady=5, sticky=W + E)
        self.save_file_btn.grid(row=0, column=1, padx=10, pady=5)
        self.output_txt.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=W + N + E + S)

    # 输入文件按钮
    def select_file(self):
        self.var_input_file = tk.filedialog.askopenfile()
        # 更新输入输出文件路径
        self.input_file_name.delete(0, END)
        self.input_file_name.insert(END, self.var_input_file.name)
        self.output_file_name.delete(0, END)
        self.var_output_name = os.path.splitext(self.var_input_file.name)[0] + '.frc'
        self.output_file_name.insert(END, self.var_output_name)
        # 更新显示
        self.update_visual()

    # 更新显示
    def update_visual(self):
        # 读取文件
        with open(self.var_input_file.name, 'r', encoding='UTF-8') as f:
            self.var_input_content = f.readlines()

        # 更新输入信息
        self.input_txt.delete(1.0, END)
        for v in self.var_input_content:
            self.input_txt.insert(END, v)

        # 转换
        try:
            self.var_output_content = regex_convert(self.var_input_content)
        except ValueError as e:
            tk.messagebox.showerror('错误', str(e))

        # 更新输出信息
        self.output_txt.delete(1.0, END)
        for v in self.var_output_content:
            self.output_txt.insert(END, v)

    # 保存文件
    def save_file(self):
        self.var_output_name = self.output_file_name.get()
        if os.path.exists(self.var_output_name):
            tk.messagebox.showwarning('警告', '文件存在，将会覆盖文件：\n' + self.var_output_name)
        with open(self.var_output_name, 'w', encoding='UTF-8') as f:
            for v in self.var_output_content:
                f.write(v)
        tk.messagebox.showinfo('完成', '保存成功')


# 定义运行代码
def main():
    root = ttk.Window(
        title='FFRenameRegexGenerator',
        # size=(1200, 600)
    )
    Application(root)
    root.mainloop()


# 运行
main()
