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


class RetroactivePriorityQueue:
    NODE_TYPE = Node

    def __int__(self):
        self._root_key = None
        self._items = dict()
        self._leaves = list()
        self._new_id = 0

    def _push_non_root(self, new_node: NODE_TYPE, subtree_root: NODE_TYPE):
        """
        insert a non-root node to tree
        :param new_node:
        :param subtree_root:
        :return:
        """
        # TODO: balance the tree
        if (subtree_root.left_key is not None) and (subtree_root.right_key is not None):
            self._update_parent_insert(parent=subtree_root, new_node=new_node)
            if new_node < subtree_root:
                self._push_non_root(new_node=new_node, subtree_root=self._items[subtree_root.left_key])
            else:
                self._push_non_root(new_node=new_node, subtree_root=self._items[subtree_root.right_key])

        else:
            if new_node < subtree_root:
                self._create_subtree(node_left=new_node, node_right=subtree_root, new='left')
            else:
                self._create_subtree(node_left=subtree_root, node_right=new_node, new='right')

    def _create_subtree(self, node_left: NODE_TYPE, node_right: NODE_TYPE, new: str):
        """
        create new subtree because of adding new node and connect it to tree
        :param node_left:
        :param node_right:
        :param new: with one is new node
        :return:
        """
        # create parent node
        range_time = (min(node_left.range_time[0], node_right.range_time[0]),
                      max(node_right.range_time[1], node_left.range_time[1]))
        parent = self.NODE_TYPE(data=node_left.data.merge(node_right.data), range_time=range_time)

        # update the range_time of children
        node_left.range_time = (node_left.range_time[0], node_right.range_time[0] - 1)
        node_right.range_time = (node_right.range_time[0], max(node_right.range_time[1], node_left.range_time[1]))

        # connect to children
        parent.right_key = node_right.range_time
        parent.left_key = node_left.range_time

        # connect to parent
        if new == 'right':
            parent.parent_key = node_left.parent_key
            self._items.pop(node_left.range_time, None)
        else:
            parent.parent_key = node_right.parent_key
            self._items.pop(node_right.range_time, None)

        self._root_key = parent.range_time if parent.parent_key is None else self._root_key
        if parent.parent_key:
            self._items[parent.parent_key].left_key = parent.range_time

        # connect children to parent
        node_right.parent_key = range_time
        node_left.parent_key = range_time

        # update node lists
        self._items.update({range_time: parent, node_right.range_time: node_right, node_left.range_time: node_left})

    def _update_parent_insert(self, parent: NODE_TYPE, new_node: NODE_TYPE):
        """
        update range_time and data of parent when a push happened
        :param parent:
        :param new_node:
        :return:
        """
        range_time = parent.range_time
        if range_time[0] < new_node.range_time[0]:
            range_time = (new_node.range_time[0], range_time[1])
        elif range_time[1] > new_node.range_time[1]:
            range_time = (range_time[0], new_node.range_time[1])

        parent.range_time = range_time
        parent.data.merge(new_node.data)
        self._items[range_time] = parent

    def _push(self, new_node):
        """
        insert a node to tree
        :param new_node:
        :return:
        """
        if self._root_key is None:
            self._root_key = new_node.range_time
            self._items.update({new_node.range_time: new_node})

        else:
            self._push_non_root(new_node=new_node, subtree_root=self._items[self._root_key])

    def _create_leaf_node(self, time: int, value) -> NODE_TYPE:
        """
        create new leaf node
        :param time:
        :param value:
        :return: new node
        """
        data = PriorityQueue(started_at=self._new_id).push(value=value, key=time)
        self._new_id += 1
        return self.NODE_TYPE(data=data, range_time=(time, time), start_operation=Operations.Push)

    def insert(self, operation, time: int, value=None):
        if operation == Operations.Push:
            # TODO check it overlaps in leaf nodes if overlap update
            new_node = self._create_leaf_node(time, value)
            self._push(new_node=new_node)
        elif operation == Operations.Pop:
            pass

    def delete(self):
        pass
