from agents.agent import Agent


class EDF_Agent(Agent):
    """ Earliest Deadline First """

    def __init__(self):
        Agent.__init__(self)

    def get_action(self, obs):
        unfinished_sfcs, vnf_ready_nodes, next_idle_time, next_idle_vms, _ = obs
        # 选择 Job 的 deadline 最小的优先
        # TODO 可能要修改：如果有 sibling vnf结点在执行，是否选择其他 vnf结点
        selected_vnf = None
        for v in vnf_ready_nodes:
            if selected_vnf is None:
                selected_vnf = v
            elif v.sfc_dag.deadline < selected_vnf.sfc_dag.deadline:
                selected_vnf = v
        return selected_vnf
