import numpy as np

from sfc_env.util import Vnf_Finished_Type


class Exec_Record:
    def __init__(self, start_time, end_time, vm_node, vnf_finished_type):
        self.start_time = start_time
        self.vm_node = vm_node
        if vnf_finished_type is Vnf_Finished_Type.Finished:
            self.finish_time = end_time
            self.finished_type = Vnf_Finished_Type.Finished
        elif vnf_finished_type is Vnf_Finished_Type.Failed:
            self.fail_time = end_time
            self.finished_type = Vnf_Finished_Type.Failed


class VNF_Node:
    def __init__(self, idx, vnf_idx, v_type, workload, redundancy, sfc):
        # id
        self.idx = idx
        # vnf 类型
        self.type = v_type
        # 在 SFC 链中的序号（0开始）
        self.vnf_idx = vnf_idx
        # [Feature] vnf 计算量
        self.workload = workload
        # [Feature] vnf 加权 deadline
        self.vnf_deadline = None
        # [Feature] 距离 deadline 时间
        self.deadline_remain = None
        # [Feature] 剩余 SFC 长度
        self.remain_len = None
        # [Feature] 冗余执行次数
        self.exec_times = 0
        # [Feature] 冗余个数
        self.redundancy = redundancy
        # [Feature] 剩余计算量
        self.remain_workload = None

        # 所属的 SFC DAG
        self.sfc = sfc
        self.sfc_idx = sfc.idx
        # 前序 VNF
        self.pre_vnf = None
        # 后续 VNF
        self.next_vnf = None
        # 运行所在的机器结点
        self.vm_node = None
        # 运行记录
        self.records = []

    def record_an_execution(self, start_time, end_time, vm_node, vnf_finished_type):
        assert len(self.records) < self.redundancy
        self.records.append(Exec_Record(start_time, end_time, vm_node, vnf_finished_type))
        self.exec_times += 1
        return self.exec_times

    def get_a_record(self, record_id):
        assert record_id > 0
        assert record_id <= self.redundancy
        return self.records[record_id-1]
