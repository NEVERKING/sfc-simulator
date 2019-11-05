from agents.edf_agent import EDF_Agent
from agents.eft_agent import EFT_Agent
from param import args
from agents.random_agent import Random_Agent
from sfc_env.env import Environment
from sfc_env.gantt_chart import plot_gantt
from sfc_env.util import check_completed, print_vms, summarize_result

from sfc_env.util import print_sfcs
from agents.sjf_agent import SJF_Agent

# agent = Random_Agent()
# agent = SJF_Agent()
# agent = EFT_Agent()
# agent = EDF_Agent()

agents = [Random_Agent(), SJF_Agent(), EFT_Agent(), EDF_Agent()]

for agent in agents:
    env = Environment()
    env.seed(args.seed)
    env.reset()
    obs = env.observe()
    print_sfcs(list(env.unfinished_sfcs))
    print_vms(env)
    done = False
    while not done:
        selected_node = agent.get_action(obs)
        obs, done = env.step(selected_node)
        print("---------------------------------")

    print("Agent:", agent.__class__)
    print("completed:", check_completed(env))
    summarize_result(env)

    plot_gantt(env)
