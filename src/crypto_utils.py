"""
密码学工具函数模块
提供哈希计算、随机数生成、秘密分割与合并等功能
"""
import hashlib
import random
from Crypto.Util import number

def generate_large_prime(bit_length=2048):
    """生成一个大素数"""
    return number.getPrime(bit_length)

def hash_function(data, prime):
    """
    哈希函数，将输入数据映射到[0, prime-1]范围内
    使用SHA-256进行哈希，然后取模
    """
    # 确保输入是字节类型
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # 计算SHA-256哈希
    sha256_hash = hashlib.sha256(data).digest()
    
    # 将哈希结果转换为整数
    hash_int = int.from_bytes(sha256_hash, byteorder='big')
    
    # 取模操作，确保结果在[0, prime-1]范围内
    return hash_int % prime

def split_secret(secret, prime):
    """
    将秘密分割为两个份额
    满足: secret ≡ share1 + share2 (mod prime)
    """
    # 随机生成第一个份额
    share1 = random.randint(0, prime - 1)
    
    # 计算第二个份额
    share2 = (secret - share1) % prime
    
    return share1, share2

def combine_shares(share1, share2, prime):
    """
    合并两个份额得到秘密
    满足: secret ≡ share1 + share2 (mod prime)
    """
    return (share1 + share2) % prime

def generate_random_number(prime):
    """生成一个[1, prime-1]范围内的随机数"""
    return random.randint(1, prime - 1)
    