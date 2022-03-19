import enum

from priority_queue import PriorityQueue


class Operations(enum.Enum):
    Push = 1
    Pop = 2


class Query(enum.Enum):
    final_queue = 1
    min_element = 2
    max_element = 3


class BaseNode:
    def __init__(self):
        self._left_key = None
        self._right_key = None
        self._parent_key = None
        self._is_leaf = False
        self.height = 0

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
        if self.left_key and self.left_key[1] > other.range_time[0]:
            return True
        return (self.range_time[0] < other.range_time[0]) or \
               (self.range_time[0] >= other.range_time[0] and self.range_time[1] < other.range_time[1])

    def __gt__(self, other):
        if self.left_key and self.left_key[1] < other.range_time[0]:
            return True
        return (self.range_time[0] > other.range_time[0]) or \
               (self.range_time[0] <= other.range_time[0] and self.range_time[1] > other.range_time[1])

    def __eq__(self, other):
        return self.range_time == other.range_time

    def __str__(self):
        start = "-".join("" for _ in range(self.height))
        spaces = " ".join("" for _ in range(self.height))
        return f"{start}Node:\n" \
               f"{spaces}range_time: {self.range_time}\n" \
               f"{spaces}operation: {self.start_operation if self.start_operation else str()}\n" \
               f"{spaces}current_data: {str(self.data)}\n" \
               f"{spaces}deleted_data: {str(self.deleted_data)}"

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

    def _change_height(self, parent_node) -> int:
        """

        :param parent_node:
        :return:
        """
        parent_node.height = 1 + max(self._items[parent_node.left_key].parent_node,
                                     self._items[parent_node.right_key].parent_node)
        self._items[parent_node.range_time] = parent_node
        return parent_node.height

    def _get_balance_value(self, subtree_root) -> int:
        """
        :param subtree_root:
        :return:
        """
        if not subtree_root:
            return 0
        return self._items[subtree_root.left_key].height - self._items[subtree_root.right_key].height

    def _balance(self, subtree_root):
        balance_value = self._get_balance_value(subtree_root)
        left_balance_value = self._get_balance_value(self._items[subtree_root.left_key])
        right_balance_value = self._get_balance_value(self._items[subtree_root.right_key])
        # left left
        if balance_value > 1 and left_balance_value > 0:
            self._rotate(subtree_root, feature_name_root='left_key', feature_name_child='right_key')

        # right right
        if balance_value < -1 and right_balance_value < 0:
            self._rotate(subtree_root, feature_name_root='right_key', feature_name_child='left_key')

        # Left Right
        if balance_value > 1 and left_balance_value < 0:
            subtree_root = self._rotate(subtree_root, feature_name_root='left_key', feature_name_child='right_key',
                                        same=False)
            self._rotate(subtree_root, feature_name_root='right_key', feature_name_child='left_key')

        # Right Left
        if balance_value < -1 and right_balance_value > 0:
            subtree_root = self._rotate(subtree_root, feature_name_root='right_key', feature_name_child='left_key',
                                        same=False)
            self._rotate(subtree_root, feature_name_root='left_key', feature_name_child='right_key')

    def _rotate(self, subtree_root, feature_name_root: str, feature_name_child: str, same=True):
        """
        in this method feature_name_root and feature_name_child are opposite
        :param subtree_root:
        :param feature_name_root: the side that is going to root
                                  for right right or right left -> right_key
                                  for left left or left right -> left_key
        :param feature_name_child: the side that is going to merge
                                  for right right or right left -> left_key
                                  for left left or left right -> right_key
        :return:
        """
        child_new_parent = self._items[getattr(self._items[getattr(subtree_root, feature_name_root)],
                                               feature_name_child)]
        if not same:
            self._update_parent_insert(parent=child_new_parent, new_node=self._items[getattr(subtree_root,
                                                                                             feature_name_child)])
        if feature_name_child == 'left_key':
            # right left or right right
            node_left = self._items[getattr(subtree_root, feature_name_child)]
            node_right = self._items[child_new_parent.left_key] if not same else child_new_parent
            new = 'left'
        else:
            # left right or left left
            node_right = self._items[getattr(subtree_root, feature_name_child)]
            node_left = self._items[child_new_parent.left_key] if not same else child_new_parent
            new = 'right'

        self._create_subtree(node_left=node_left, node_right=node_right, new=new)
        node = self._items[getattr(subtree_root, feature_name_root)]
        subtree_root.right_key = node.right_key
        subtree_root.left_key = node.left_key
        self._items.pop(node.range_time)
        self._items[subtree_root.range_time] = subtree_root
        return subtree_root

    def _push_non_root(self, new_node: NODE_TYPE, subtree_root: NODE_TYPE):
        """
        insert a non-root node to tree
        :param new_node:
        :param subtree_root:
        :return:
        """

        if (subtree_root.left_key is not None) and (subtree_root.right_key is not None):
            self._update_parent_insert(parent=subtree_root, new_node=new_node)
            if new_node < subtree_root:
                self._push_non_root(new_node=new_node, subtree_root=self._items[subtree_root.left_key])
            else:
                self._push_non_root(new_node=new_node, subtree_root=self._items[subtree_root.right_key])

            self._change_height(subtree_root)
            self._balance(subtree_root=subtree_root)

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

        self._change_height(parent)

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

    def _update_parent_delete(self, child_node: NODE_TYPE):
        """

        :param child_node:
        :return:
        """
        parent = self._items[child_node.parent_key]
        merged_node = self._items[parent.left_key].merge(self._items[parent.right_key])
        parent.update_range(start=merged_node.range_time[0], end=merged_node.range_time[1])
        parent.data = merged_node.data
        parent.deleted_data = parent.deleted_data
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

    def _delete_sub_tree(self, node):
        parent = self._items.pop(node.parent_key)
        other_child = self._items.pop(parent.left_key if parent.right_key == node.range_time else parent.right_key)
        other_child.parent_key = parent.parent_key
        self._items[other_child.range_time] = other_child
        return other_child

    def delete(self, time: int):
        """
        delete a operation from tree
        :param time:
        :return:
        """
        all_leaves = self._get_all_leaves()
        if time in [key[0] for key in all_leaves]:
            key = [key for key in all_leaves if key[0] == time][0]
            deleted_node = self._items.pop(key)
            if key == self._root_key:
                self._root_key = False
            else:
                key = self._delete_sub_tree(deleted_node).range_time
                while key:
                    node = self._items[key]
                    self._update_parent_delete(child_node=node)
                    self._change_height(node)
                    self._balance(node)
                    key = node.parent_key

    def _find_all_ranges(self, subtree_root: NODE_TYPE, time: int) -> set:
        """
        find all ranges that the make (- inf, time)
        :param subtree_root:
        :param time:
        :return: a set of Node
        """
        result = set()
        if subtree_root.range_time[1] <= time:
            result.add(subtree_root)

        elif subtree_root.range_time[0] > time:
            result.add(self.NODE_TYPE(range_time=(-float('inf'), time)))

        elif subtree_root.left_key is not None and subtree_root.right_key is not None:
            if time > subtree_root.left_key[1]:
                result.add(self._items[subtree_root.left_key])
                result.add(self._find_all_ranges(self._items[subtree_root.right_key], time))
            else:
                result.add(self._find_all_ranges(self._items[subtree_root.left_key], time))

        else:
            result.add(subtree_root)

        return result

    def _get_data_until_time(self, time: int) -> NODE_TYPE:
        """
        get all ranges and make node (-inf, time)
        :param time:
        :return: a node
        """
        all_ranges = self._find_all_ranges(self._items[self._root_key], time)
        final_node = min(all_ranges)
        all_ranges.remove(final_node)
        while all_ranges:
            min_node = min(all_ranges)
            final_node.merge(min_node, apply=True)
            all_ranges.remove(min_node)
        final_node.update_range(start=final_node.range_time[0], end=time)
        return final_node

    def query(self, time: int, query: Query):
        """
        query operation
        :param time:
        :param query:
        :return:
        """
        node = self._get_data_until_time(time)
        if query == Query.final_queue:
            return node.data
        if query == Query.min_element:
            return node.data.min_value

    def print_tree(self, subtree_root: NODE_TYPE):
        """
        print subtree
        :param subtree_root: subtree_root node
        :return:
        """
        if subtree_root.is_leaf:
            print(subtree_root)
        else:
            self.print_tree(self._items[subtree_root.left_key])
            print(subtree_root)
            self.print_tree(self._items[subtree_root.right_key])

