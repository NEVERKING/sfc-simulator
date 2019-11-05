from collections import OrderedDict
from enum import Enum, unique

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def check_completed(env):
    return not (len(env.sfc_generator) or len(env.unfinished_sfcs) or len(env.vnf_ready_nodes))


def summarize_result(env):
    print('可靠完成:', len(env.completed_sfcs))
    print('达到时延:', len(env.satisfied_deadline_sfcs))
    print('平均时延:', np.mean([s.completion_time for s in env.completed_sfcs]))
    print('成功的平均时延:', np.mean([s.completion_time for s in env.satisfied_deadline_sfcs]))


def print_vms(env):
    print([v.speed for v in env.vm_nodes])


def print_sfcs(sfcs):
    for s in sfcs:
        print('SFC:', s.idx, 'VNF:', [v.type for v in s.vnfs], 'Rel:', s.rel_list)


def print_vnfs(vnfs):
    for v in vnfs:
        print("vnf idx: %s, vnf type: %s, vnf workload: %s, redundancy: %s" % (v.idx, v.type, v.workload, v.redundancy))


def plot_distribution(data):
    plt.hist(data, bins=40, facecolor="blue", edgecolor="black", alpha=0.7)
    plt.show()


@unique
class Vnf_State(Enum):
    Waiting = 0
    Ready = 1
    Running = 2
    Completed = 3
    Failed = 4


@unique
class Vnf_Finished_Type(Enum):
    Finished = 0
    Free = 1
    Failed = 2


@unique
class Vm_State(Enum):
    Idle = 0
    Finishing = 1  # just finish
    Running = 2


class printable:
    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gather_attrs())

    def gather_attrs(self):
        return ",".join("\n{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())


class OrderedSet:
    def __init__(self, contents=()):
        self.set = OrderedDict((c, None) for c in contents)

    def __contains__(self, item):
        return item in self.set

    def __iter__(self):
        return iter(self.set.keys())

    def __len__(self):
        return len(self.set)

    def add(self, item):
        self.set[item] = None

    def clear(self):
        self.set.clear()

    def index(self, item):
        idx = 0
        for i in self.set.keys():
            if item == i:
                break
            idx += 1
        return idx

    def pop(self):
        item = next(iter(self.set))
        del self.set[item]
        return item

    def remove(self, item):
        del self.set[item]

    def to_list(self):
        return [k for k in self.set]

    def update(self, contents):
        for c in contents:
            self.add(c)


def plot_dag(sfcs):
    G = nx.DiGraph()
    G.add_nodes_from(range(sfcs.num_nodes))
    for i in range(sfcs.num_nodes):
        for j in range(sfcs.num_nodes):
            if sfcs.adj_mat[i, j] == 1:
                G.add_edge(i, j)
    print(sfcs.adj_mat)
    nx.draw(G, pos=nx.shell_layout(G))
    plt.show()


def child_and_siblings(sfcs):
    print(sfcs.adj_mat)
    for i in sfcs.nodes:
        print(i.idx, "child:", [j.idx for j in i.child_nodes])
        print(i.idx, ":", [j.idx for j in i.sibling_nodes])
