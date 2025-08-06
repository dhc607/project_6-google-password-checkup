"""
服务器模块
实现服务器和辅助服务器的功能
"""
from .crypto_utils import hash_function, split_secret, generate_random_number, combine_shares

class Server:
    """主服务器类，维护泄露密码数据库并参与协议"""
    
    def __init__(self, prime):
        """初始化服务器"""
        self.prime = prime
        self.leaked_passwords = set()  # 泄露密码集合
        self.shares = {}  # 存储服务器持有的秘密份额: {password: (s1, s2)}
    
    def add_leaked_password(self, password):
        """添加泄露的密码并计算其秘密份额"""
        if password not in self.leaked_passwords:
            self.leaked_passwords.add(password)
            # 计算密码的哈希值
            password_hash = hash_function(password, self.prime)
            # 分割哈希值为两个份额
            s1, s2 = split_secret(password_hash, self.prime)
            self.shares[password] = (s1, s2)
    
    def prepare_challenge(self):
        """生成挑战值k"""
        return generate_random_number(self.prime)
    
    def verify_response(self, response, challenge, r1):
        """
        验证响应是否表明密码已泄露
        如果存在某个泄露密码，使得 (k * s1 + r1) mod prime == response，则密码已泄露
        """
        k = challenge
        for password in self.leaked_passwords:
            s1, _ = self.shares[password]
            if (k * s1 + r1) % self.prime == response:
                return True
        return False


class HelperServer:
    """辅助服务器类，存储秘密份额并参与协议"""
    
    def __init__(self, prime):
        """初始化辅助服务器"""
        self.prime = prime
        self.shares = {}  # 存储辅助服务器持有的秘密份额: {password: s2}
    
    def receive_share(self, password, s2):
        """接收并存储主服务器发送的秘密份额s2"""
        self.shares[password] = s2
    
    def process_query(self, t2, challenge):
        """
        处理客户端查询
        生成r2和响应值
        """
        k = challenge
        # 生成随机数r2
        r2 = generate_random_number(self.prime)
        
        # 计算响应值response = (k * s2 + r2) mod prime，其中s2是与t2匹配的份额
        # 遍历所有份额查找匹配项
        response = None
        for s2 in self.shares.values():
            if (t2 - s2) % self.prime == 0:  # 检查是否匹配
                response = (k * s2 + r2) % self.prime
                break
        
        # 如果没有找到匹配项，随机生成一个响应
        if response is None:
            # 随机选择一个份额计算响应（为了隐藏是否存在匹配）
            random_s2 = next(iter(self.shares.values())) if self.shares else 0
            response = (k * random_s2 + r2) % self.prime
        
        return r2, response
    