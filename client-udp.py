import socket

# 配置目标服务器信息
SERVER_IP = '61.172.168.122'   # 目标服务器IP
SERVER_PORT = 9999        # 目标服务器端口
MESSAGE = b'Hello UDP!'   # 要发送的消息 (字节字符串)

# 创建UDP socket并发送消息
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(MESSAGE, (SERVER_IP, SERVER_PORT))
print(f"已向 {SERVER_IP}:{SERVER_PORT} 发送 {len(MESSAGE)} 字节")
client.close()