import numpy as np

from param import args
from sfc_env.vnf_node import VNF_Node


class Sfc:
    def __init__(self, idx, vnfs, deadline, reliability, arrived_time):
        # SFC index
        self.idx = idx
        # vnf 原始序列（数组）
        self.vnf_list = vnfs
        # SFC 长度
        self.sfc_len = len(self.vnf_list)
        # 截止时间
        self.deadline = deadline
        # 可靠性要求
        self.reliability = reliability
        # 可靠性列表
        self.rel_list = self.gen_redundancy_list()
        # 总计算量
        self.total_workload = self.get_total_workload()

        # 是否到达
        self.arrived = False
        # 是否成功完成（可靠）
        self.completed = False
        # 是否已经失败（不可靠）
        self.isFailed = False
        # 开始时间（到达时间）
        self.start_time = arrived_time
        # 完成时间
        self.completion_time = np.inf

        # VNF队列
        self.vnfs = self.gen_vnf_list()
        self.head = self.vnfs[0]
        self.ready_vnf = self.get_ready_vnf(0)

    def update_arrived_state(self, time):
        if time >= self.start_time and not self.arrived:
            self.arrived = True
            self.ready_vnf = self.vnfs[0]

    def get_ready_vnf(self, time):
        self.update_arrived_state(time)
        # SFC 已经到达，且没有失败
        if self.arrived and not self.isFailed:
            return self.ready_vnf

    def go_forward_to_next_vnf(self):
        self.ready_vnf = self.ready_vnf.next_vnf

    def gen_redundancy_list(self):
        rel_list = [1] * self.sfc_len
        index = 0
        while self.rel(rel_list) < self.reliability:
            rel_list[index] = rel_list[index] + 1
            index = (index + 1) % self.sfc_len
        # print([i for i in rel_list])
        return rel_list

    def rel(self, rel_list):
        r = 1
        for i in range(self.sfc_len):
            r = r * (1 - pow((1 - args.rel), rel_list[i]))
        return r

    def gen_vnf_list(self):
        vnf_nodes = []

        # 1. vnf 按照计算量排序
        sorted_vnfs = sorted(self.vnf_list, key=lambda a: a.workload)
        # 2. 排序后分配冗余
        for index, v in enumerate(sorted_vnfs):
            v.redundancy = self.rel_list[index]
        # 3. 按照 vnf id 排序（执行先后）
        sorted_vnfs = sorted(sorted_vnfs, key=lambda a: a.idx)
        # 4. 生成 VNF 冗余列表
        self.rel_list = list(map(lambda a: a.redundancy, sorted_vnfs))

        # 创建 VNF 结点
        for index, v in enumerate(sorted_vnfs):
            node = VNF_Node(index, v.idx, v.type, v.workload, v.redundancy, self)
            vnf_nodes.append(node)

        # 创建 VNF 结点前序后序关系
        for i in range(len(vnf_nodes) - 1):
            pre = vnf_nodes[i]
            nex = vnf_nodes[i + 1]
            pre.next_vnf = nex
            nex.pre_vnf = pre

        return vnf_nodes

    def get_total_workload(self):
        return sum([v.workload for v in self.vnf_list])
