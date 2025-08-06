"""
Google Password Checkup协议测试
验证协议的正确性和安全性特性
"""
import pytest
from src.protocol import run_protocol
from src.crypto_utils import generate_large_prime

# 固定一个测试用的素数，确保测试的一致性
TEST_PRIME = generate_large_prime(bit_length=2048)

# 测试用的泄露密码列表
TEST_LEAKED_PASSWORDS = [
    "password123", 
    "qwerty", 
    "123456", 
    "letmein"
]

def test_leaked_password_detection():
    """测试协议能否正确检测已泄露的密码"""
    # 测试每个泄露的密码
    for pwd in TEST_LEAKED_PASSWORDS:
        assert run_protocol(TEST_LEAKED_PASSWORDS, pwd, TEST_PRIME) is True

def test_non_leaked_password_detection():
    """测试协议能否正确识别未泄露的密码"""
    # 测试未泄露的密码
    non_leaked_passwords = [
        "securepassword",
        "MyP@ssw0rd!",
        "1234567890abcdef",
        ""  # 空密码
    ]
    
    for pwd in non_leaked_passwords:
        assert run_protocol(TEST_LEAKED_PASSWORDS, pwd, TEST_PRIME) is False

def test_empty_leaked_list():
    """测试当泄露列表为空时的情况"""
    assert run_protocol([], "anypassword", TEST_PRIME) is False

def test_case_sensitivity():
    """测试协议是否区分大小写（应该区分）"""
    # 添加一个小写密码到泄露列表
    leaked = ["testpassword"]
    
    # 检查相同小写密码（应检测为泄露）
    assert run_protocol(leaked, "testpassword", TEST_PRIME) is True
    
    # 检查大写版本（不应检测为泄露）
    assert run_protocol(leaked, "TestPassword", TEST_PRIME) is False
    