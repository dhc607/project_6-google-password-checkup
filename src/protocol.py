"""
协议核心逻辑模块
协调客户端、服务器和辅助服务器之间的交互
"""
from .client import Client
from .server import Server, HelperServer
from .crypto_utils import generate_large_prime

def run_protocol(leaked_passwords, client_password, prime=None):
    """
    运行Google Password Checkup协议
    参数:
        leaked_passwords: 泄露的密码列表
        client_password: 客户端要检查的密码
        prime: 大素数，若为None则自动生成
    返回:
        bool: 密码是否已泄露
    """
    # 生成大素数（如果未提供）
    if prime is None:
        prime = generate_large_prime()
    
    # 初始化参与方
    server = Server(prime)
    helper = HelperServer(prime)
    client = Client(prime)
    
    # 服务器添加泄露的密码并与辅助服务器共享秘密份额
    for pwd in leaked_passwords:
        server.add_leaked_password(pwd)
        _, s2 = server.shares[pwd]
        helper.receive_share(pwd, s2)
    
    # 协议步骤
    # 1. 客户端处理密码，生成两个份额
    t1, t2 = client.process_password(client_password)
    
    # 2. 服务器生成挑战值
    challenge = server.prepare_challenge()
    
    # 3. 客户端将t2发送给辅助服务器，辅助服务器处理并返回r2和response
    r2, response = helper.process_query(t2, challenge)
    
    # 4. 客户端计算r1
    r1 = client.compute_r1(t1, r2)
    
    # 5. 服务器验证响应
    is_leaked = server.verify_response(response, challenge, r1)
    
    return is_leaked
    