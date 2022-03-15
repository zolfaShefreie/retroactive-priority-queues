from priority_queue import PriorityQueue


class Node:
    def __init__(self, data: PriorityQueue, range_time: tuple, start_operation=None):
        self.range_time = range_time
        self.data = data
        self.start_operation = start_operation # that means the operation occurs in time = range_time[0

    def __lt__(self, other):
        return (self.range_time[0] < other.range_time[0]) or \
               (self.range_time[0] == other.range_time[0] and self.range_time[1] < other.range_time[1])

    def __eq__(self, other):
        return self.range_time == other.range_time

    def update_range(self, start, end):
        self.range_time = (start, end)


class RetroactivePriorityQueue:
    pass