import itertools

import numpy as np

from param import *
from sfc_env.sfc import Sfc
from sfc_env.sfc_queue import SFC_Queue
from sfc_env.vnf import Vnf


def gen_sfc_requests(np_random, workloads, speed_avg, reliables):
    # 1. 一开始就在队列中的
    sfc_requests = SFC_Queue()
    t = 0
    counter = itertools.count()
    for _ in range(args.num_init_sfc):
        sfc_request = gen_a_sfc_request(np_random, next(counter), workloads, speed_avg, reliables, t)
        sfc_requests.push(t, sfc_request)
    # 2. 中途随机到达的
    for _ in range(args.num_stream_dags):
        # poisson process 泊松到达过程
        t += np_random.exponential(args.stream_interval)
        # generate job
        sfc_request = gen_a_sfc_request(np_random, next(counter), workloads, speed_avg, reliables, t)
        # push into timeline
        sfc_requests.push(t, sfc_request)
    return sfc_requests


# 生成 SFC 请求（包括sfc链和时延，可靠性要求）
def gen_a_sfc_request(np_random, idx, workloads, speed_avg, reliables, time):
    # 1. sfc 长度
    sfc_len = gen_sfc_length(np_random, args.len_avg, args.len_sigma)
    # 2. sfc 的 vnf
    chain = gen_sfc_seq(np_random, len(workloads), sfc_len)
    vnfs = []
    total_workload = 0
    for index, c in enumerate(chain):
        vnfs.append(Vnf(index, c, workload=workloads[c]))
        total_workload += workloads[c]
    # 3. 时延
    deadline = gen_sfc_deadline(np_random, speed_avg, total_workload)
    # 4. 可靠性
    reliability = gen_sfc_reliability(np_random, reliables)
    return Sfc(idx, vnfs, deadline, reliability, time)


# 随机生成 SFC 长度（正态分布，均值和标准差）
def gen_sfc_length(np_random, avg, sigma):
    sfc_len = 0
    while sfc_len <= 1 or sfc_len > 8:
        sfc_len = int(np_random.normal(loc=avg, scale=sigma, size=None))
        # print(sfc_len)
    return sfc_len


def gen_sfc_seq(np_random, vnf_types, sfc_len):
    # 长度和类型数量给定，选取不同类型的 vnf
    types = list(range(vnf_types))
    # return random.sample(types, sfc_len)
    return np_random.choice(types, size=sfc_len, replace=None)
    # return [np_random.randint(0, vnf_types - 1) for _ in range(sfc_len)]


def gen_sfc_deadline(np_random, speed_avg, total_workload):
    # 平均的完成时间
    avg_complete_time = total_workload / speed_avg
    # 平均的 deadline
    avg_deadline = avg_complete_time * 1.4
    # 以平均 deadline为均值 的正态分布
    deadline = round(np_random.normal(loc=avg_deadline, scale=0.5), 2)
    while deadline < avg_complete_time:
        deadline = round(np_random.normal(loc=avg_deadline, scale=0.5), 2)
    return deadline


def gen_sfc_reliability(np_random, rel_list):
    # 在一个可选择的列表里面随机选取一个
    return np_random.choice(rel_list)


if __name__ == '__main__':

    sfc = gen_a_sfc_request(np.random, 0, [40, 20, 15, 10, 30, 35, 45, 25], 10, [0.95, 0.99, 0.999, 0.9995], 10)
    print(sfc)
    for i in sfc.vnfs:
        print("------------")
        print(i)
