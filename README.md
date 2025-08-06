# Google Password Checkup 协议实现

本项目实现了Google Password Checkup验证协议，基于论文《Privacy-Preserving Password Checking with Secret Sharing》(https://eprint.iacr.org/2019/723.pdf) 中section 3.1描述的协议。该协议允许用户检查自己的密码是否在泄露密码列表中，同时保护用户密码隐私和泄露密码数据库的安全性。

## 协议概述

Google Password Checkup协议旨在解决隐私保护的密码检查问题：如何让用户检查自己的密码是否在泄露密码列表中，同时不泄露用户密码和具体的泄露密码信息。

协议涉及三个参与方：
- 客户端(Client)：用户侧，拥有待检查的密码
- 服务器(Server)：维护泄露密码数据库
- 辅助服务器(Helper Server)：协助完成密码检查

核心思想是使用秘密共享技术，将密码哈希值分割为多个份额，由不同参与方持有，通过协作完成比对而不泄露完整信息。

## 安装说明

### 环境要求

- Python 3.6 或更高版本

### 安装依赖
pip install -r requirements.txt
## 使用方法

### 运行演示程序
python examples/demo.py
演示程序将展示协议的基本功能，检查两个示例密码（一个已泄露，一个未泄露）并输出结果。

### 在自己的项目中使用
from src.protocol import run_protocol

# 泄露的密码列表
leaked_passwords = ["password123", "qwerty", "123456"]

# 要检查的密码
client_password = "mysecretpassword"

# 运行协议
is_leaked = run_protocol(leaked_passwords, client_password)

print(f"密码{'已泄露' if is_leaked else '未泄露'}")
## 运行测试
pytest tests/test_protocol.py -v
测试将验证协议的基本功能和安全性特性。


    
