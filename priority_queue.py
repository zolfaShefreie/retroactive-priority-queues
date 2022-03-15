

class QueueElement:

    def __init__(self, put_index, value):
        self.put_index = put_index
        self.value = value

    def __eq__(self, other):
        return self.put_index == other.id and self.value == other.value

    def __lt__(self, other):
        return (self.value < other.value) or \
               (self.value == self.value and self.put_index < self.put_index)


class PriorityQueue:

    def __init__(self):
        pass