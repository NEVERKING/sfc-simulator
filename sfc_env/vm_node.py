from sfc_env.util import Vm_State
import numpy as np


class VM:
    """
     VM 结点
    """

    def __init__(self, idx, speed):
        self.idx = idx
        self.speed = speed
        self.state = Vm_State.Idle
        self.next_idle_time = 0.0
        self.last_vnf_type = None
        self.last_vnf = None
        self.last_sfc = None
        self.last_completion_time = 0.0

        # 待初始化
        self.current_vnf = None
        self.current_sfc = None
        self.vnf_record_id = None
        self.vnf_finished_type = None

    def assign_a_vnf(self, sfc, vnf, end_time, vnf_finished_type, record_id):
        self.current_sfc = sfc
        self.current_vnf = vnf
        # end_time 可以是失败时间，也可以是成功执行完成时间
        self.next_idle_time = end_time
        self.state = Vm_State.Running
        self.vnf_finished_type = vnf_finished_type
        self.vnf_record_id = record_id

    def update_vm_status(self, time):
        if time == self.next_idle_time:  # 此时刚好完成，env 需要更新信息
            self.last_vnf_type = self.current_vnf.type if self.current_vnf is not None else None
            self.last_vnf = self.current_vnf
            self.last_completion_time = self.next_idle_time
            self.state = Vm_State.Finishing  # 正好完成
        elif time > self.next_idle_time:
            self.state = Vm_State.Idle  # 之前已经完成，现在是空闲
        elif time < self.next_idle_time:
            self.state = Vm_State.Running  # 此时还在运行

    def reset(self):
        self.last_vnf = self.current_vnf
        self.last_sfc = self.current_sfc
        self.current_vnf = None
        self.current_sfc = None
        self.next_idle_time = 0.0

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gather_attrs())

    def gather_attrs(self):
        return ",".join("\n{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())
