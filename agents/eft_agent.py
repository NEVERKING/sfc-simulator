from agents.agent import Agent
from sfc_env.env import expected_complete_time_at_vm
import numpy as np


class EFT_Agent(Agent):
    """ Earliest Finish First """

    def __init__(self):
        Agent.__init__(self)

    def get_action(self, obs):
        unfinished_sfcs, vnf_ready_nodes, next_idle_time, next_idle_vms, _ = obs
        # Earliest Finish Time 选择最早可以完成的 VNF 优先
        # TODO 可能要修改：如果有 sibling vnf结点在执行，是否选择其他 vnf结点
        eft = np.inf
        selected_vnf = None
        for v in vnf_ready_nodes:
            tmp = min([expected_complete_time_at_vm(next_idle_time, vm, v)[0] for vm in next_idle_vms])
            if tmp < eft:
                eft = tmp
                selected_vnf = v
        return selected_vnf
