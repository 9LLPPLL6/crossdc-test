import os
import time
import argparse

def test_io_performance(file_path, file_size_mb, operation):
    """
    测试读写性能
    :param file_path: 测试文件路径
    :param file_size_mb: 文件大小(MB)
    :param operation: 'write' 或 'read'
    :return: 带宽 MB/s
    """
    block_size = 1024 * 1024  # 1MB块大小
    total_bytes = file_size_mb * block_size
    data = os.urandom(block_size)  # 生成随机数据块

    start_time = time.time()

    if operation == 'write':
        with open(file_path, 'wb') as f:
            for _ in range(file_size_mb):
                f.write(data)
                f.flush()  # 确保数据写入磁盘
                os.fsync(f.fileno())  # 强制同步到存储
    
    elif operation == 'read':
        with open(file_path, 'rb') as f:
            while f.read(block_size):  # 循环读取直到结束
                pass

    elapsed = time.time() - start_time
    return file_size_mb / elapsed  # MB/s

def main():
    parser = argparse.ArgumentParser(description='测试远程存储读写带宽')
    parser.add_argument('--size', type=int, default=1024, help='测试文件大小(MB) 默认1024MB')
    parser.add_argument('--clean', action='store_true', help='测试完成后删除文件')
    args = parser.parse_args()

    test_file = "/mnt/hpfs/bandwidth_test.bin"
    file_size_mb = args.size

    print(f"测试文件: {test_file}")
    print(f"文件大小: {file_size_mb} MB")

    # 写入测试
    write_speed = test_io_performance(test_file, file_size_mb, 'write')
    print(f"写入带宽: {write_speed:.2f} MB/s")

    # 读取测试
    read_speed = test_io_performance(test_file, file_size_mb, 'read')
    print(f"读取带宽: {read_speed:.2f} MB/s")

    # 清理测试文件
    if args.clean:
        os.remove(test_file)
        print("测试文件已删除")

if __name__ == "__main__":
    main()