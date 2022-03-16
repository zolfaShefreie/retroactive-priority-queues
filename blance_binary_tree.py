

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
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

    def __lt__(self, other):
        return self.value < other.value


class BalancedTree:
    NODE_TYPE = Node

    def __int__(self):
        self._root = None
        self._items = dict()

    def _get_new_key(self) -> int:
        """
        generate new key for new node
        :return: new key
        """
        return max(self._items.keys()) + 1 if len(self._items) else 0

    def _insert_non_root(self, new_node: NODE_TYPE, subtree_root: NODE_TYPE):
        """
        insert a non-root node to tree
        :param new_node:
        :param subtree_root:
        :return:
        """
        if new_node < subtree_root:
            if subtree_root.left_key is None:
                subtree_root.left_key = new_node.key
                new_node.parent_key = subtree_root.key
                self._items.update({new_node.key: new_node})
            else:
                self._insert_non_root(new_node=new_node, subtree_root=self._items[subtree_root.left_key])
        else:
            if subtree_root.right_key is None:
                subtree_root.right_key = new_node.key
                new_node.parent_key = subtree_root.key
                self._items.update({new_node.key: new_node})
            else:
                self._insert_non_root(new_node=new_node, subtree_root=self._items[subtree_root.right_key])

    def insert(self, value):
        """
        insert a node to tree
        :param value:
        :return:
        """
        new_node = self.NODE_TYPE(key=self._get_new_key(), value=value)
        if self._root is None:
            self._root = new_node
            self._items.update({new_node.key: new_node})

        else:
            self._insert_non_root(new_node=new_node, subtree_root=self._root)

    def delete(self):
        pass
