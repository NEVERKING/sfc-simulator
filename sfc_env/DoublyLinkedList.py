class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append_all(self, datalist):
        for data in datalist:
            self.append(data)

    def append(self, data):
        new_node = Node(data)
        # last = self.head
        # new_node.next = None
        if self.head is None:
            # new_node.prev = None
            self.head = new_node
            self.tail = new_node
            return
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.head
        new_node.prev = None
        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node

    def print_elements(self):
        last = self.head
        if self.head is None:
            return
        else:
            while last:
                print(last.data, end=" ")
                last = last.next

        print()
        res = self.tail
        if self.tail is None:
            return
        else:
            while res:
                print(res.data, end=" ")
                res = res.prev

    def insert_after(self, prevnode, data):
        new_node = Node(data)
        new_node.next = prevnode.next
        prevnode.next = new_node
        new_node.prev = prevnode
        if new_node.next is not None:
            new_node.next.prev = new_node

    def delete(self, prevnode):
        if prevnode is None:
            return
        if prevnode == self.head:
            self.head = prevnode.next
        if prevnode.next is None:
            self.tail = prevnode.prev
        if prevnode.next is not None:
            prevnode.next.prev = prevnode.prev
        if prevnode.prev is not None:
            prevnode.prev.next = prevnode.next


if __name__ == '__main__':
    llist = LinkedList()
    llist.append(1)
    llist.append(2)
    llist.push(0)
    llist.append(3)
    llist.append(4)

    llist.append(5)
    llist.append(6)
    llist.delete(llist.head.next)
    # llist.insertafter(llist.head.next,8)
    llist.print_elements()
