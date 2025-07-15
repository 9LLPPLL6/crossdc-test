import os
import argparse
import torch
import torch.distributed as dist
import torch_npu

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("--rank", type=int, help="进程的rank (0 或 1)")
    parser.add_argument("--master_addr", default="127.0.0.1", help="主节点IP地址")
    parser.add_argument("--master_port", default="29500", help="主节点端口")
    args = parser.parse_args()

    # 初始化分布式环境
    os.environ['MASTER_ADDR'] = args.master_addr
    os.environ['MASTER_PORT'] = args.master_port
    
    # 使用TCP后端，设置全局进程组
    dist.init_process_group("hccl", rank=args.rank, world_size=2)
    
    # 设置当前使用的NPU设备
    torch.npu.set_device(f"npu:{args.rank}")
    device = torch.device(f"npu:{args.rank}")
    
    print(f"进程 {args.rank} 在 NPU{args.rank} 上运行")

    # 定义要发送的数据
    if args.rank == 0:
        data = torch.ones(1024, 1024, device=device) * 42.0  # 创建一个1024x1024的浮点张量
        recv_data = torch.zeros_like(data)
    else:
        data = torch.zeros(1024, 1024, device=device)
        recv_data = torch.zeros_like(data)

    # 进程0发送给进程1，同时进程1接收
    if args.rank == 0:
        # 发送数据到rank1
        dist.send(data, dst=1)
        print(f"Rank {args.rank}: 已发送数据到Rank 1")
        
        # 接收来自rank1的数据
        dist.recv(recv_data, src=1)
        print(f"Rank {args.rank}: 已从Rank 1接收数据")
        
        # 验证接收的数据
        print(f"接收的数据平均值: {recv_data.mean().item()}")
    else:
        # 接收来自rank0的数据
        dist.recv(recv_data, src=0)
        print(f"Rank {args.rank}: 已从Rank 0接收数据")
        
        # 创建要发送的数据
        send_data = torch.ones_like(recv_data) * 99.0
        
        # 发送数据回rank0
        dist.send(send_data, dst=0)
        print(f"Rank {args.rank}: 已发送数据到Rank 0")
        
        # 保存接收的数据用于验证
        data.copy_(recv_data)
        print(f"接收的数据平均值: {recv_data.mean().item()}")

    # 清理分布式环境
    dist.destroy_process_group()

if __name__ == "__main__":
    main()