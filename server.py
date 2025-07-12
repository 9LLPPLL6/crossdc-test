import socket

# 创建TCP套接字
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))  # 绑定所有接口的12345端口
server.listen(1)  # 开始监听，允许1个连接排队

print(" TCP服务器已启动，等待连接...")

while True:
    client, addr = server.accept()  # 接受客户端连接
    print(f"🔌 客户端已连接: {addr[0]}:{addr[1]}")
    
    try:
        while True:
            data = client.recv(1024)  # 接收数据
            if not data: break  # 客户端断开连接
            print(f"📨 收到数据: {data.decode()}")
            client.sendall(data)  # 原样返回数据
    finally:
        client.close()  # 关闭客户端连接
        print(f"🔌 连接已关闭")