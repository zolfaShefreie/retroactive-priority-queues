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
        self._is_leaf = False

    def _update_is_leaf(self):
        self._is_leaf = True if self._right_key or self._left_key else False

    @property
    def is_leaf(self):
        return self._is_leaf

    @property
    def right_key(self):
        return self._right_key

    @right_key.setter
    def right_key(self, value: int):
        self._right_key = value
        self._update_is_leaf()

    @property
    def left_key(self):
        return self._left_key

    @left_key.setter
    def left_key(self, value: int):
        self._left_key = value
        self._update_is_leaf()

    @property
    def parent_key(self):
        return self._parent_key

    @parent_key.setter
    def parent_key(self, value: int):
        self._parent_key = value


class Node(BaseNode):
    def __init__(self, range_time: tuple, data=None, deleted_data=None, start_operation=None):
        super().__init__()
        self.range_time = range_time
        self.data = data if data else PriorityQueue()
        self.deleted_data = deleted_data if deleted_data else PriorityQueue()
        self.start_operation = start_operation # that means the operation occurs in time = range_time[0]

    def __lt__(self, other):
        return (self.range_time[0] < other.range_time[0]) or \
               (self.range_time[0] == other.range_time[0] and self.range_time[1] < other.range_time[1])

    def __eq__(self, other):
        return self.range_time == other.range_time

    def update_range(self, start, end):
        self.range_time = (start, end)

    def merge(self, other, apply=False):
        """
        merge the data and delete_data and return new Node or apply on self
        :param apply:
        :param other:
        :return:
        """
        l_node = other if other < self else self
        g_node = self if self < other else other
        union_queue = l_node.data.union(g_node.deleted_data)
        queue_1, queue_2 = union_queue.split_queue(union_queue.kth_min(k=len(g_node.deleted_data)))
        data = g_node.data.union(queue_1)
        deleted_data = l_node.deleted_data.union(queue_2)
        if apply:
            self.data = data
            self.deleted_data = deleted_data
            self.update_range(start=min(self.range_time[0], other.range_time[0]),
                              end=max(self.range_time[1], other.range_time[1]))
            return self
        else:
            return Node(range_time=(min(self.range_time[0], other.range_time[0]),
                                    max(self.range_time[1], other.range_time[1])),
                        data=data, deleted_data=deleted_data)

    def update(self, new_value, operation: Operations):
        """
        update node data based on queue's element's changes
        :param operation:
        :param new_value:
        :return:
        """
        self.start_operation = operation
        if len(self.data) > 0:
            pre_item = self.data.min_value
            self.data.remove(pre_item)
            self.data.push(new_value, pre_item.put_index)
        elif len(self.deleted_data) > 0:
            pre_value = self.deleted_data.min_value
            self.deleted_data.remove(pre_value)
            self.deleted_data.push(new_value, pre_value.put_index)

        all_elements = self.data.union(self.deleted_data)
        len_deleted = len(self.deleted_data)
        self.data, self.deleted_data = all_elements.split_queue(all_elements.kth_min(k=len_deleted))


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
        parent = node_right.merge(node_left)

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
        node_right.parent_key = parent.range_time
        node_left.parent_key = parent.range_time

        # update node lists
        self._items.update({parent.range_time: parent,
                            node_right.range_time: node_right,
                            node_left.range_time: node_left})

    def _update_parent_insert(self, parent: NODE_TYPE, new_node: NODE_TYPE):
        """
        update range_time and data of parent when a push happened
        :param parent:
        :param new_node:
        :return:
        """
        self._items.pop(parent.range_time)
        parent.merge(new_node, apply=True)
        self._items[parent.range_time] = parent

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

    def _create_leaf_node(self, time: int, value, operation: Operations) -> NODE_TYPE:
        """
        create new leaf node
        :param time:
        :param value:
        :return: new node
        """
        data = PriorityQueue(started_at=self._new_id).push(value=value, key=time)
        self._new_id += 1
        if operation == Operations.Pop:
            self.NODE_TYPE(deleted_data=data, range_time=(time, time), start_operation=operation)
        else:
            return self.NODE_TYPE(data=data, range_time=(time, time), start_operation=operation)

    def _get_all_leaves(self):
        """
        :return: a list of leaf keys
        """
        return [key for key, value in self._items.items() if value.is_leaf]

    def insert(self, operation: Operations, time: int, value=None):
        """
        insert a node to tree
        :param operation:
        :param time:
        :param value:
        :return:
        """
        value = value if value else float('inf')
        all_leaves = self._get_all_leaves()
        if time in [key[0] for key in all_leaves]:
            key = [key for key in all_leaves if key[0] == time][0]
            self._update(operation=operation, key=key, value=value)
        else:
            new_node = self._create_leaf_node(time, value, operation)
            self._push(new_node=new_node)

    def _update(self, operation, key, value=None):
        """
        overwrite one the node and it affection on tree
        :param operation:
        :param key:
        :param value:
        :return:
        """
        while key:
            node = self._items.pop(key)
            node.update(value, operation)
            self._items[key] = node
            key = node.parent_key

    def delete(self):
        pass
