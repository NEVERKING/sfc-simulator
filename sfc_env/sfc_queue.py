import heapq
import itertools


class SFC_Queue:
    """记录 SFC 的到达情况"""

    def __init__(self):
        # 优先队列
        self.pq = []
        # 计数器
        self.counter = itertools.count()

    def __len__(self):
        return len(self.pq)

    def peek(self):
        # 如果优先队列有内容，返回第一个
        if len(self.pq) > 0:
            (key, counter, item) = self.pq[0]
            return key, item
        # 如果没有东西，返回
        else:
            return None, None

    def push(self, key, item):
        """根据 key堆排序，key为到达时间"""
        heapq.heappush(self.pq,
                       (key, next(self.counter), item))

    def pop(self):
        """取出当前最早到达的 sfc"""
        if len(self.pq) > 0:
            (key, counter, item) = heapq.heappop(self.pq)
            return key, item
        else:
            return None, None

    def get_arrived_sfcs(self, current_time):
        return [sfc for sfc in self.pq if sfc.start_time <= current_time]

    def get_waiting_sfcs(self, current_time):
        """
        SFC 等待队列：已经到达，未完成，并且没有失败（可靠性）
        """
        return [sfc for sfc in self.pq if
                sfc.start_time <= current_time and sfc.completed is False and sfc.failed is False]

    def reset(self):
        self.pq = []
        self.counter = itertools.count()
