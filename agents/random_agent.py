from agents.agent import Agent
import numpy as np


class Random_Agent(Agent):
    def __init__(self):
        Agent.__init__(self)

    def get_action(self, obs):
        unfinished_sfcs, vnf_ready_nodes, next_idle_time, next_idle_vms, _ = obs

        selected_vnf = np.random.choice(list(vnf_ready_nodes))

        return selected_vnf
