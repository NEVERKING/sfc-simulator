from agents.agent import Agent


class SJF_Agent(Agent):
    """ Shortest Job First """

    def __init__(self):
        Agent.__init__(self)

    def get_action(self, obs):
        unfinished_sfcs, vnf_ready_nodes, next_idle_time, next_idle_vms, _ = obs
        # 选择 Job 的 total workload最小的优先
        # 为了保证 set是有序的（每次测试都一样）
        # TODO 可能要修改：如果有 sibling vnf结点在执行，是否选择其他 vnf结点
        vnf_ready_nodes = sorted(vnf_ready_nodes, key=lambda a: (a.sfc_dag.idx, a.idx))
        selected_vnf = None
        for v in vnf_ready_nodes:
            if selected_vnf is None:
                selected_vnf = v
            elif v.sfc_dag.total_workload < selected_vnf.sfc_dag.total_workload:
                selected_vnf = v
        return selected_vnf
