class Record:
    def __init__(self, idx, start, end, event, vnf_node):
        self.idx = idx
        self.start = start
        self.end = end
        self.event = event
        self.vnf_node = vnf_node

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self.gather_attrs())

    def gather_attrs(self):
        return ",".join("\n{}={}"
                        .format(k, getattr(self, k))
                        for k in self.__dict__.keys())



class Schedule_Record:

    def __init__(self, vms):
        self.vms = [[] * 0 for _ in range(len(vms))]

    def record(self, idx, start, end, event, vnf_node):
        a = Record(idx, start, end, event, vnf_node)
        self.vms[idx].append(a)


if __name__ == '__main__':
    s = Schedule_Record([0, 1, 2, 3, 4, 5, 6])
    s.record(1,1.5,2,'start','node1')
