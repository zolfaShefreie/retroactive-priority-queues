

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
    type_element = QueueElement

    def __init__(self, started_at: int, save_list=True):
        self.__save_list = save_list
        self.__next_id = started_at
        self.__set_items = set()
        self.__min_value = None

    def get_min(self):
        """
        get the minimum of
        :return: QueueElement object
        """
        return self.__min_value

    def pop(self):
        """
        delete the minimum item in queue
        :return:
        """
        self.__set_items.remove(self.__min_value)
        self._set_min()

    def _set_min_with_element(self, element: type_element):
        """
        set min based on new element
        :param element:
        :return:
        """
        self.__min_value = self.__min_value if self.__min_value < element else element

    def _set_min(self):
        """
        set min based on items
        :return:
        """
        self.__min_value = min(self.__set_items)

    def push(self, value, key=None):
        """
        insert new value to queue
        :param key:
        :param value:
        :return: a boolean
        """
        element = self.type_element(push_index=key if key else self.__next_id, value=value)
        self.__set_items.add(element)
        self.__next_id += 1
        self._set_min_with_element(element)

    def __eq__(self, other):
        """

        :param other:
        :return: a boolean
        """
        return not (self.__set_items ^ other.__set_items)

    def merge(self, other):
        pass
