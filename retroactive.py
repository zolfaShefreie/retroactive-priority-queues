import enum

from priority_queue import PriorityQueue


class Operations(enum.Enum):
    Push = 1
    Pop = 2


class BaseNode:
    def __init__(self):
        self._left_key = None
        self._right_key = None
        self._parent_key = None

    @property
    def right_key(self):
        return self._right_key

    @right_key.setter
    def right_key(self, value: int):
        self._right_key = value

    @property
    def left_key(self):
        return self._left_key

    @left_key.setter
    def left_key(self, value: int):
        self._left_key = value

    @property
    def parent_key(self):
        return self._parent_key

    @parent_key.setter
    def parent_key(self, value: int):
        self._parent_key = value


class Node(BaseNode):
    def __init__(self, data: PriorityQueue, range_time: tuple, start_operation=None):
        super().__init__()
        self.range_time = range_time
        self.data = data
        self.start_operation = start_operation # that means the operation occurs in time = range_time[0]

    def __lt__(self, other):
        return (self.range_time[0] < other.range_time[0]) or \
               (self.range_time[0] == other.range_time[0] and self.range_time[1] < other.range_time[1])

    def __eq__(self, other):
        return self.range_time == other.range_time

    def update_range(self, start, end):
        self.range_time = (start, end)


