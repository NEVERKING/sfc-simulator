import numpy as np

from param import args, speed_list, speed_weights, workload_list, reliable_list
from sfc_env.sfc_generator import gen_sfc_requests
from sfc_env.sfc_queue import SFC_Queue
from sfc_env.util import Vnf_Finished_Type, Vm_State
from sfc_env.vm_generator import gen_vm, get_avg_vm_speed


def expected_complete_time_at_vm(time, vm, vnf_node):
    process_time = vnf_node.workload / vm.speed
    # 1. 计算开始时间：
    # 看之前执行的 VNF 类型，如果相同不处理，如果不同则需要保证 开始执行的时间与之前的结束时间相隔 delta
    if vm.last_vnf_type is None:  # 第一次执行
        start_time = time
    elif vm.last_vnf_type != vnf_node.type:
        start_time = max(time, vm.last_completion_time + args.delta)
    else:
        start_time = time
    # 2. 计算完成时间
    completion_time = start_time + process_time
    return completion_time, start_time


class Environment:

    def __init__(self):
        # 独立随机数生成器
        self.np_random = np.random.RandomState()
        # SFC 任务生成队列 (所有未到达的)
        self.sfc_generator = SFC_Queue()
        # SFC 已经到达的(未完成的 SFC)
        self.unfinished_sfcs = set()
        # SFC 已经失败的
        self.failed_sfcs = set()
        # SFC 已经完成的
        self.completed_sfcs = set()
        # SFC 达到时延要求的
        self.satisfied_deadline_sfcs = set()
        # 已经 Ready 的 VNF
        self.ready_vnfs = set()
        # 机器结点
        self.vm_nodes = []

        # for computing reward at each step
        # self.reward_calculator = RewardCalculator()

    def reset(self):
        self.unfinished_sfcs = set()  # 已经到达，未完成的 SFC
        self.failed_sfcs = set()  # 已经失败的 SFC（可靠性）
        self.completed_sfcs = set()  # 已经完成的 SFC
        self.ready_vnfs = set()  # Ready 的 VNF
        # 机器结点
        self.vm_nodes = gen_vm(self.np_random, args.num_vm, speed_list, speed_weights)
        self.sfc_generator = gen_sfc_requests(self.np_random, workload_list,
                                              get_avg_vm_speed(self.vm_nodes),
                                              reliable_list)
        # 初始化 0 时刻的 [未完成] 和 [Ready VNF]
        self.add_to_unfinished_set_and_ready_set(time=0)

    def observe(self):
        idle_time, idle_vms = self.get_next_idle_vms()
        return self.unfinished_sfcs, self.ready_vnfs, idle_time, idle_vms, False

    def step(self, selected_vnf):
        """
        执行一步动作
        1. 将选中的 VNF分配到一台机器上
        2. 更新队列、机器的状态（持续更新至 [有idle机器] 以及 [Ready VNF非空] 的时刻）
        :param selected_vnf: 选中的 VNF
        :return: 最早的 [有idle机器] 以及 [Ready VNF非空] 的时刻
        """
        print("选中的 vnf_node:", (selected_vnf.idx, selected_vnf.sfc_idx))
        # 获取最早完成的 VM 结点
        idle_time, selected_vm = self.select_a_vm(selected_vnf)
        print("空闲时间:", idle_time)
        print("选中的机器:", selected_vm.idx)
        # 选好了以后，分配该 VNF到节点上
        self.assign(selected_vnf, selected_vm, idle_time)

        # 然后再获取下一个 idle 时间，使用该时间更新所有的结点信息
        # 这个 idle 时间可以是某个 VNF失败，可以是执行完成的时间，选择在此时更新所有 VNF和 VM节点状态
        # ① 看这个 VNF如果是执行成功的，那么：
        #   1. 从队列中移除这个 VNF，执行成功
        #   2. 其它已经开始的冗余 VNF的完成时间更新，其机器的完成时间更新，设置状态为 Free
        #   3. 如果是同时完成的 VNF，则先检查到的 VNF为成功，其他的为 Free
        # ② 如果是一个失败的 VNF：
        #   1. 看是否所有冗余全部失败，如果全部失败，那么 SFC Failed
        #   2. 如果没有全部失败，不做处理

        # 分配 VNF 之后，再移动至下一个 idle 时刻
        next_idle_time = self.step_inside()

        # todo 如果下一个 idle时刻有新的 SFC到达，则加入 SFC和 VNF队列
        self.add_to_unfinished_set_and_ready_set(time=next_idle_time)

        while self.block_by_no_ready_sfc():  # 被 Ready队列阻塞（Ready为空）
            # 更新时间到下一个Ready 非空的时间
            print("+++++++++++++++++++")
            if len(self.sfc_generator) != 0:  # 后续还有 SFC请求
                print("后续还有 SFC请求")
                # 比较下一个 VM释放时间 还是 SFC请求到达时间 早
                next_arrived_time, _ = self.sfc_generator.peek()  # 查看下一个 SFC到达的时刻
                peek_next_idle_time, _ = self.get_next_idle_vms_after(next_idle_time)
                if next_arrived_time <= peek_next_idle_time:
                    # 如果下一个 SFC请求较早到达，那么先加入到 SFC 队列中
                    print("加入 SFC请求")
                    self.add_to_unfinished_set_and_ready_set(time=next_arrived_time)
                else:  # 如果下个SFC请求到达比 VM释放更晚，则先释放
                    # 如果时间没有继续更新了，就说明释放已经到头了，
                    if peek_next_idle_time == next_idle_time:
                        print("释放已经到头了")
                        next_idle_time = next_arrived_time
                    else:
                        print("释放")
                        next_idle_time = self.step_inside(True, next_idle_time)
            else:  # 后续没有到达的 SFC了
                next_idle_time = self.step_inside(True, next_idle_time)
                # # 如果时间没有继续更新了，就说明已经到头了
                # if next_idle_time == last_time:
                #     return None, True
                # last_time = next_idle_time

        done = not self.ready_vnfs and not self.unfinished_sfcs and len(self.sfc_generator) == 0

        print("vnf_ready_nodes:", [(v.idx, v.sfc_dag.idx) for v in self.ready_vnfs])
        print("unfinished_sfcs:", [s.idx for s in self.unfinished_sfcs])

        return self.observe(), done

    def block_by_no_ready_sfc(self):
        return not self.ready_vnfs and (len(self.sfc_generator) != 0 or self.unfinished_sfcs)

    def step_inside(self, inside=False, min_time=0):
        """
        :param inside: True：表示之前时间没有 Ready VNF，需要继续推进时间
        :param min_time: 上一个 idle时刻
        :return: 下一个 idle时刻
        """
        if not inside:
            next_idle, next_idle_vms = self.get_next_idle_vms()
        else:
            next_idle, next_idle_vms = self.get_next_idle_vms_after(min_time)
        # 将机器的状态更新到下一个 idle时刻
        self.update_vms_at_next_idle(next_idle)

        # 需要检查的 vm结点：
        # 在该时刻 finishing 的 vm（不包括原来就 idle的以及被中断的 vm）
        finishing_vms = [vm for vm in next_idle_vms if vm.state is Vm_State.Finishing]

        print("分配以后下个空闲时间:", next_idle)
        print("在该时间点空闲的机器个数:", len(finishing_vms))
        print("在该时间点释放的机器:", [v.idx for v in finishing_vms])

        for vm in finishing_vms:
            vnf = vm.last_vnf
            print("完成的 VNF:", (vnf.idx, vnf.sfc_idx, vm.vnf_finished_type))
            if vm.vnf_finished_type is Vnf_Finished_Type.Finished:  # 成功而 idle的
                # 告知同级结点，更新相关机器的 idle时间
                vnf.update_redundancy_finish_time(vm.vnf_record)
                # 如果该 vnf有后继结点，加入 Ready队列呀，如果没有的话 SFC就执行完了呢
                if vnf.next_vnf:
                    self.add_to_ready_set(vnf.next_vnf)
                    print('添加的后续结点:', (vnf.next_vnf.idx, vnf.next_vnf.sfc_idx))
                else:  # 没有后继结点，说明执行完毕
                    vnf.sfc.completion_time = next_idle
                    self.completed_sfcs.add(vnf.sfc)
                    if next_idle <= vnf.sfc.deadline:  # 如果达到了时延要求
                        self.satisfied_deadline_sfcs.add(vnf.sfc)
                    self.unfinished_sfcs.discard(vnf.sfc)
                    vnf.sfc.completed = True
                    print("完成SFC:", vnf.sfc.idx)
            elif vm.vnf_finished_type is Vnf_Finished_Type.Failed:  # 由于失败而 idle的
                if vnf.is_all_failed():  # 如果全失败了，SFC 失败
                    self.set_an_sfc_failed(vnf.sfc)
        return next_idle

    def update_vms_at_next_idle(self, next_idle):
        for vm in self.vm_nodes:
            vm.update_vm_status(next_idle)

    def set_an_sfc_failed(self, sfc):
        sfc.isFailed = True  # SFC 失败
        self.unfinished_sfcs.discard(sfc)
        self.failed_sfcs.add(sfc)
        print("失败SFC:", sfc)

    def select_a_vm(self, selected_vnf):
        # 所有空闲的 vm
        idle_time, idle_vms = self.get_next_idle_vms()
        # 选择最早完成的 vm
        sort_vms = sorted(idle_vms, key=lambda vm: expected_complete_time_at_vm(idle_time, vm, selected_vnf))
        return idle_time, sort_vms[0]

    def add_to_unfinished_set_and_ready_set(self, time):
        """
        根据输入的时间（下一个空闲机器时刻），将到达的 SFC放入到达队列
        """
        arrived_time, _ = self.sfc_generator.peek()
        if arrived_time is None:  # 说明没有新的 SFC了
            return
        # 如果有在 time时刻前到达的，就加入集合
        while arrived_time <= time:
            _, sfc = self.sfc_generator.pop()
            # 加入Unfinished SFC
            self.unfinished_sfcs.add(sfc)
            # 加入Ready VNF
            self.ready_vnfs.add(sfc.head)
            arrived_time, _ = self.sfc_generator.peek()
            if arrived_time is None:  # 说明没有新的 SFC了
                return

    def add_to_ready_set(self, ready_vnf):
        self.ready_vnfs.add(ready_vnf)

    def get_next_idle_vms(self):
        """ 获取下一个有机器空闲的时间 """
        # 获取最早的 idle时间
        next_idle = min(map(lambda v: v.next_idle_time, self.vm_nodes))
        # 获取 idle时间的机器
        next_idle_vms = [v for v in self.vm_nodes if v.next_idle_time == next_idle]
        return next_idle, next_idle_vms

    def get_next_idle_vms_after(self, min_time):
        """ 获取下一个有机器空闲的时间 """
        # 获取最早的 idle时间
        vms = [v.next_idle_time for v in self.vm_nodes if v.next_idle_time > min_time]
        if not vms:  # 如果没有在这之后转为空闲的机器了，说明已经执行完了（不能继续推进了）
            next_idle_vms = [v for v in self.vm_nodes if v.next_idle_time <= min_time]
            return min_time, next_idle_vms
        else:
            next_idle = min(vms)
            # 获取 idle时间的机器
            next_idle_vms = [v for v in self.vm_nodes if v.next_idle_time <= next_idle]
            return next_idle, next_idle_vms

    def assign(self, vnf, vm, time):
        """
        分配过程中，需要修改VNF和VM的状态等信息，同时要注意是否执行成功（可靠性）
        """
        succeed = args.rel >= self.np_random.random()  # 是否成功
        completion_time, start_time = expected_complete_time_at_vm(time, vm, vnf)
        # 2.1 如果成功，设置 vnf结点的完成时间
        if succeed:
            # 记录执行信息
            record = vnf.record_an_execution(start_time, completion_time, vm, Vnf_Finished_Type.Finished)
            # 更新 vm 结点的信息
            vm.assign_a_vnf(vnf.sfc, vnf, completion_time, record)

        # 2.2 如果失败，设置 vnf结点的失败时间
        else:
            fail_time = self.np_random.uniform(start_time, completion_time)  # 计算失败的时间点
            # 记录执行信息
            exec_id = vnf.record_an_execution(start_time, fail_time, vm, Vnf_Finished_Type.Failed)
            # 更新 vm 结点的信息
            vm.assign_a_vnf(vnf.sfc, vnf, fail_time, exec_id)

    def seed(self, seed):
        self.np_random.seed(seed)



