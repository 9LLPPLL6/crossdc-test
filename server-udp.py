import socket

def run_udp_server(host='0.0.0.0', port=9999):
    """
    启动UDP服务器
    :param host: 监听的主机地址 (默认监听所有可用接口)
    :param port: 监听的端口 (默认9999)
    """
    # 创建UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # 绑定到指定地址和端口
        sock.bind((host, port))
        print(f"UDP服务器已启动，正在监听 {host}:{port}...")
        
        while True:
            # 接收数据 (缓冲区大小设为1024字节)
            data, addr = sock.recvfrom(1024)
            print(f"收到来自 {addr[0]}:{addr[1]} 的数据包，长度: {len(data)} 字节")
            
            # 可选：发送响应
            # sock.sendto(b"Server received: " + data, addr)
    
    except KeyboardInterrupt:
        print("\n服务器被手动终止")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        sock.close()
        print("UDP服务器已关闭")

if __name__ == '__main__':
    # 示例：监听本地回环地址的9999端口
    run_udp_server(port=9999)