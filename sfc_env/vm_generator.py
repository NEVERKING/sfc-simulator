import numpy as np
from sfc_env.vm_node import VM


def gen_vm(np_random, num, speed_list, speed_weight):
    speeds = gen_vm_speeds(np_random, num, speed_list, speed_weight)
    vm_nodes = []
    for index, s in enumerate(speeds):
        vm_node = VM(index, s)
        vm_nodes.append(vm_node)
    return vm_nodes


def gen_vm_speeds(np_random, num, speed_list, speed_weight):
    # return random.choices(speed_list, weights=speed_weight, k=num)
    return np_random.choice(speed_list, size=num, replace=True, p=[0.14,0.23,0.28,0.35])


def get_avg_vm_speed(vms):
    return np.mean([v.speed for v in vms])
