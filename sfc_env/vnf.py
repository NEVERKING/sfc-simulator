

class Vnf:
    def __init__(self, idx, v_type, workload):
        # vnf 类型
        self.type = v_type
        # 在 SFC 链中的序号（0开始）
        self.idx = idx
        # vnf 计算量
        self.workload = workload
        # 冗余数量, 默认为 1
        self.redundancy = 1



