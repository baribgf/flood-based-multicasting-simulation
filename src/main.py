from typing import Self
from threading import Thread, Condition

from util import report

class Node:
    def __init__(self, id: int, is_master=False) -> None:
        self.id = id
        self._is_master = is_master
        self._neighbors: set[Self] = set()
        self._rec_from: set[Self] = set()
        self._received = Condition()
        self._thread = None

    def _workload(self):
        report("Node %d alive" % self.id)
        if self._is_master:
            return
        
        self._received.acquire()
        self._received.wait()
        self.broadcast()
        self._received.release()

    def deploy(self):
        thread = Thread(
            target=self._workload,
            name="Thread-%d" % self.id
        )
        self._thread = thread
        thread.start()

    def broadcast(self):
        report("Node %d broadcasting.." % self.id)
        for neigh in self._neighbors:
            if neigh not in self._rec_from:
                neigh.receive(self)
                report(
                    "Node %d sent message "
                    "to Node %d" % (self.id, neigh.id)
                )

    def receive(self, other: Self):
        self._rec_from.add(other)
        self._received.acquire()
        self._received.notify()
        self._received.release()

    def connect(self, *others):
        self._neighbors.update(set(others))

    def wait(self):
        self._thread.join()
        report("Node %d is dead" % self.id)

def main():
    v0 = Node(0, True)
    v1 = Node(1)
    v2 = Node(2)
    v3 = Node(3)
    v4 = Node(4)
    v5 = Node(5)
    v6 = Node(6)

    v0.connect(v1, v2, v3)
    v1.connect(v0, v4)
    v2.connect(v0, v3)
    v3.connect(v0, v2, v4, v5, v6)
    v4.connect(v1, v3, v5)
    v5.connect(v3, v4)
    v6.connect(v2, v3)

    graph = {
        v0, v1, v2, v3,
        v4, v5, v6
    }

    for node in graph:
        node.deploy()

    # start the broadcast with master node
    v0.broadcast()

    # wait and announce for node death
    for node in graph:
        node.wait()

if __name__ == '__main__':
    main()
