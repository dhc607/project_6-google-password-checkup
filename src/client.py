"""
客户端模块
实现用户端的功能，包括密码处理和协议参与
"""
from .crypto_utils import hash_function, split_secret, generate_random_number

class Client:
    """客户端类，处理用户密码并参与协议"""
    
    def __init__(self, prime):
        """初始化客户端"""
        self.prime = prime
    
    def process_password(self, password):
        """
        处理用户密码，生成两个份额
        返回: (t1, t2) 满足 t1 + t2 ≡ H(password) (mod prime)
        """
        # 计算密码的哈希值
        password_hash = hash_function(password, self.prime)
        
        # 将哈希值分割为两个份额
        t1, t2 = split_secret(password_hash, self.prime)
        
        return t1, t2
    
    def compute_r1(self, t1, r2):
        """
        计算r1值
        r1 = (t1 - r2) mod prime
        """
        return (t1 - r2) % self.prime
    