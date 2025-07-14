import os
import torch
import torch.distributed as dist
import torch_npu  # 确保已安装昇腾适配的PyTorch

def setup(rank, world_size, master_addr, master_port):
    # 设置环境变量
    os.environ['MASTER_ADDR'] = master_addr
    os.environ['MASTER_PORT'] = str(master_port)
    os.environ['WORLD_SIZE'] = str(world_size)
    os.environ['RANK'] = str(rank)

    # 初始化分布式后端（使用昇腾的hccl）
    dist.init_process_group(
        backend='hccl',   # 华为集群通信库
        rank=rank,
        world_size=world_size
    )
    torch.npu.set_device(rank)  # 绑定当前进程到对应NPU设备

def cleanup():
    dist.destroy_process_group()

def main(rank, world_size, master_addr="192.168.1.1", master_port=29500):
    # 示例配置（请根据实际修改）：
    # master_addr: 主节点IP (例如第一台服务器IP)
    # world_size: 总设备数 = 2服务器 * 8卡 = 16
    
    setup(rank, world_size, master_addr, master_port)
    
    try:
        # 创建示例张量（不同rank创建不同值）
        tensor = torch.ones(1).npu() * (rank + 1)  # 使用昇腾NPU设备
        
        print(f"Rank {rank} 初始值: {tensor.cpu().numpy()}")
        
        # 执行all-reduce操作（求和）
        dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
        
        print(f"Rank {rank} 聚合后值: {tensor.cpu().numpy()}")
        
    finally:
        cleanup()

if __name__ == "__main__":
    # 实际启动需通过torchrun或分布式启动工具
    # 示例手动设置（实际通过启动器传递参数）
    world_size = 16  # 总卡数
    master_ip = "192.168.1.1"  # 主服务器IP
    # 注意：实际rank和每个进程的local_rank由启动器自动分配