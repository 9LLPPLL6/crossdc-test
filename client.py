import socket

# 创建TCP套接字
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('183.78.180.56', 12345))  # 连接到服务器IP和端口

print("✅ 已连接到服务器")

# 发送数据
client.sendall(b"Hello Server!")

# 接收响应
response = client.recv(1024)
print(f"📨 收到响应: {response.decode()}")

client.close()  # 关闭连接
print("🔌 连接已关闭")