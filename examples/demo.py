"""
Google Password Checkup协议演示
展示协议的完整运行流程
"""
from src.protocol import run_protocol
from src.crypto_utils import generate_large_prime

def main():
    # 生成一个大素数（实际应用中应使用更大的素数）
    prime = generate_large_prime(bit_length=2048)
    
    # 泄露的密码列表
    leaked_passwords = [
        "password123", 
        "qwerty", 
        "123456", 
        "letmein", 
        "welcome", 
        "monkey",
        "sunshine",
        "football"
    ]
    
    # 测试1：检查一个已泄露的密码
    test_password1 = "qwerty"
    result1 = run_protocol(leaked_passwords, test_password1, prime)
    print(f"测试1 - 密码 '{test_password1}': {'已泄露' if result1 else '未泄露'}")
    
    # 测试2：检查一个未泄露的密码
    test_password2 = "MySecurePassword123!"
    result2 = run_protocol(leaked_passwords, test_password2, prime)
    print(f"测试2 - 密码 '{test_password2}': {'已泄露' if result2 else '未泄露'}")

if __name__ == "__main__":
    main()
    