# FFRenameRegexGenerator

本项目为使用 python3 编写的 FFRenamePro 的正则表达式更名命令批量生成器。

## 使用
本项目可以使用直接使用 start.py 文件（需要安装 Python3 并添加到环境变量），或使用 Releases 的 exe 文件。

所需文件如下：

- 程序主体：start.py / FFRenameRegexGenerator.exe
- 正则表达式列表

### 正则表达式列表要求

文件需要使用 UTF-8 Without BOM 编码。

文件内容的格式如下：

```
# 这是注释
(.*)(\(.*[漢汉]化.?\))(.*)
$1$3
```

- 无内容的行不处理，跳过
- `#` 开头的行为注释行，不处理，跳过
- `(` 开头的行视为匹配正则表达式
- 正则表达式下一行为替换模板（请包含 '$x' 变量）
- 请严格按照上述开头和顺序编写 regex.txt

  >`$1` 匹配正则表达式第一个括号内的内容，`$2` 匹配第二个括号，依此类推。
  > 
  > 本工具不会校验正则表达式，请保证编写的正则式满足你的需求。
  > 
  > 正则表达式的下方必须是模板行，可以有注释和空行分割，但不能再次出现正则表达式。
  > 
  > 上部的代码表示把文件名中 `汉化` 或 `漢化` 挨着右括号或间隔一个字符的小括号里面的内容删除。

### 使用源码

拖动正则表达式列表文件到 start.py

直接运行的情况，将会读取当前文件夹下的 regex.txt

在当前目录运行：

```shell
python start.py
```

#### 打包 exe 文件

可使用 pyinstaller 包，用如下命令将会在 `./dist/` 目录下创建 windows 可执行程序：

```shell
pyinstaller -F --icon=icon.ico start.py
```

### 使用封装版

拖动正则表达式列表文件到  FFRenameRegexGenerator.exe

直接运行的情况，将会读取当前文件夹下的 regex.txt

## 输出

若正常运行后将会在当前文件夹生成 regex.frc 文件，可将此文件导入 FFRenamePro 中运行批处理命名。
