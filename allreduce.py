import os
import argparse
import torch
import torch.distributed as dist
import torch_npu  # 昇腾NPU支持

def init_distributed(backend='hccl'):
    """初始化分布式环境，返回当前rank和总world_size"""
    # 从环境变量获取参数（由torchrun自动设置）
    rank = int(os.environ['RANK'])
    local_rank = int(os.environ['LOCAL_RANK'])
    world_size = int(os.environ['WORLD_SIZE'])
    master_addr = os.environ.get('MASTER_ADDR', '127.0.0.1')
    master_port = os.environ.get('MASTER_PORT', '29500')
    
    print(f"Rank {rank} 初始化: addr={master_addr}:{master_port}, local_rank={local_rank}")
    
    # 配置分布式环境
    os.environ['MASTER_ADDR'] = master_addr
    os.environ['MASTER_PORT'] = master_port
    
    dist.init_process_group(
        backend=backend,
        rank=rank,
        world_size=world_size
    )
    
    # 绑定当前进程到对应NPU设备
    torch.npu.set_device(local_rank)
    device = torch.npu.current_device()
    
    print(f"Rank {rank}/{world_size} 准备就绪 (NPU:{device})")
    return rank, world_size, device

def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    
    try:
        # 初始化分布式环境
        rank, world_size, device = init_distributed(backend='hccl')
        
        # 创建示例张量（不同rank创建不同值）
        tensor = torch.ones(1).npu(device) * (rank + 1)  # 将张量放到对应NPU
        
        print(f"Rank {rank} 初始值: {tensor.cpu().numpy()}", flush=True)
        
        # 执行all-reduce操作（求和）
        dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
        
        # 强制刷新输出确保立即显示
        print(f"Rank {rank} 聚合后值: {tensor.cpu().numpy()}", flush=True)
        
    except Exception as e:
        print(f"Rank {rank} 发生错误: {str(e)}", flush=True)
    finally:
        dist.destroy_process_group()

if __name__ == "__main__":
    main()