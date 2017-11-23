## SUTDN
SUT Dormitory Network Command Line Tool

## Prerequisites

* [Python 2.7.13](https://www.python.org/downloads/)

## Install

In the root of the repository, where `requirements.txt` locates:

```bash
py -2 -m pip install -r requirements.txt
```

## Usage

### Online:
1. Replace `<username>` & `<password>` in `demo/online.py` with your **username** & **password**
2. Run `demo/online.py`
3. If online successfully, then run `heartbeat.py` to keep-alive

### Offline:
Run `demo/offline.py`

## Todo
- [ ] kill

# 中文版本

## SUTDN
沈阳工业大学宿舍网络命令行工具

## 条件

* [Python 2.7.13](https://www.python.org/downloads/)

## 安装

在存储库的根目录中，`requirements.txt`所在的位置处运行：

```bash
py -2 -m pip install -r requirements.txt
```

## 用法

### 上线：
1. 用你的**用户名**和**密码**替换`demo/online.py`中的`<username>`&`<password>`
2. 运行 `demo/online.py`
3. 如果成功上线，然后运行`heartbeat.py`保持在线状态

### 下线：
运行`demo/offline.py`


## 将来或许完成的功能
- [ ] 强制下线
