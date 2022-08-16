#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Subj: FFRenameRegexGenerator
# @File: start.py
# @Date: 2022/8/16 11:23

# 读取正则表达式列表

print('读取文件...')
try:
    f = open('regex.txt', 'r', encoding='UTF-8')
except FileNotFoundError:
    print('regex.txt 文件未找到')
    raise FileNotFoundError('regex.txt 文件未找到')
except UnicodeDecodeError:
    print('编码不正确，请使用 UTF-8 (without BOM) 编码的文件')
    raise UnicodeError('编码不正确，请使用 UTF-8 (without BOM) 编码的文件')
else:
    regex_list = f.readlines()
    f.close()

# 去除换行
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

file0 = ';===========================================================\n' \
        ';批处理命令文件\n;菲菲更名宝贝 之 得意非凡 (FFRename Professional)\n;菲菲的家(ffhome.com)版权所有\n;\n' \
        ';说明：本文件为系统生成，除非明白各参数之意义，否则请不要随\n;      意改动，以免影响原有的更名结果！\n' \
        ';===========================================================\n'

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
with open('regex.frc', 'w', encoding='UTF-8-SIG') as f:
    f.write(file)

print('已生成文件 regex.frc')
