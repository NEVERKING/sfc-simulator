import numpy as np

from sfc_env.util import Vnf_Finished_Type, Vm_State


class Exec_Record:
    def __init__(self, start_time, end_time, vm_node, vnf_finished_type):
        self.start_time = start_time
        self.vm_node = vm_node
        self.finish_time = end_time
        self.finished_type = vnf_finished_type


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
        return self.records[self.exec_times - 1]

    def get_a_record(self, record_id):
        assert record_id > 0
        assert record_id <= self.redundancy
        return self.records[record_id - 1]

    def update_redundancy_finish_time(self, record):
        for i, r in enumerate(self.records):
            if not (record is r) and record.finish_time <= r.finish_time:
                print('中断其它冗余:', i)
                r.finish_time = record.finish_time
                r.finish_type = Vnf_Finished_Type.Free
                r.vm_node.next_idle_time = record.finish_time
                r.vm_node.last_completion_time = record.finish_time
                r.vm_node.state = Vm_State.Idle

    def is_all_failed(self):
        for r in self.records:
            if not (r.finish_type is Vnf_Finished_Type.Failed):
                return True
        else:
            return False
