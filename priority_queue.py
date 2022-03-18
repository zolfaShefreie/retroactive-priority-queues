

class QueueElement:

    def __init__(self, push_index: int, value):
        self.put_index = push_index
        self.value = value

    def __eq__(self, other):
        return self.put_index == other.id and self.value == other.value

    def __lt__(self, other):
        return (self.value < other.value) or \
               (self.value == self.value and self.put_index < self.put_index)


class PriorityQueue:
    ELEMENT_TYPE = QueueElement

    def __init__(self, started_at=0, items=None, save_list=True):
        self._save_list = save_list
        self._next_id = started_at
        self.set_items = set(items) if items else set()
        self._min_value = self._set_min() if items else None

    @property
    def min_value(self):
        return self._min_value

    def get_min(self):
        """
        get the minimum of
        :return: QueueElement object
        """
        return self._min_value

    def pop(self):
        """
        delete the minimum item in queue
        :return:
        """
        self.set_items.remove(self._min_value)
        self._set_min()

    def _set_min_with_element(self, element: ELEMENT_TYPE):
        """
        set min based on new element
        :param element:
        :return:
        """
        self._min_value = self._min_value if self._min_value < element else element

    def _set_min(self):
        """
        set min based on items
        :return:
        """
        self._min_value = min(self.set_items)

    def push(self, value, key=None):
        """
        insert new value to queue
        :param key:
        :param value:
        :return: a boolean
        """
        element = self.ELEMENT_TYPE(push_index=key if key else self._next_id, value=value)
        self.set_items.add(element)
        self._next_id += 1
        self._set_min_with_element(element)

    def union(self, other):
        return PriorityQueue(items=self.set_items.union(other.set_items))

    def __eq__(self, other):
        """

        :param other:
        :return: a boolean
        """
        return not (self.set_items ^ other.set_items)

    def __len__(self):
        return len(self.set_items)

    def kth_min(self, k: int):
        """
        find k'th minimum of queue
        :param k:
        :return:
        """
        new_set = set(self.set_items)
        for i in range(k-1):
            new_set.remove(max(new_set))
        return max(new_set)

    def split_queue(self, split_element: ELEMENT_TYPE):
        """
        split the queue
        :param split_element:
        :return:
        """
        return PriorityQueue(items=[x for x in self.set_items if x <= split_element]), \
               PriorityQueue(items=[x for x in self.set_items if x > split_element])
