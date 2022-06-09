#!/usr/bin/python

# from __future__ import unicode_literals  # at top of module
# from __future__ import division, print_function, with_statement
from pathlib import Path
from utils.strings import string_similar


def get_path_list(path: str):
    return path.lstrip('/').rstrip('/').split('/')


class TreeNode(object):
    """
    The basic node of tree structure
    Ref: https://blog.csdn.net/xuelians/article/details/79999284
    """

    def __init__(self, name='', parent=None):
        super(TreeNode, self).__init__()
        self.name = name
        self.parent = parent
        self.child = {}
        self._temp_path_list = []

    def __repr__(self):
        return 'TreeNode(%s)' % self.name

    def __contains__(self, item):
        return item in self.child

    def __len__(self):
        """return number of children node"""
        return len(self.child)

    def __bool__(self):
        """always return True for exist node"""
        return True

    @property
    def path(self):
        """return path string (from root to current node)"""
        if self.parent:
            return '%s/%s' % (self.parent.path.strip(), self.name)

        return self.name

    def get_child(self, name, defval=None):
        """get a child node of current node"""
        return self.child.get(name, defval)

    def add_child(self, name, obj=None):
        """add a child node to current node"""

        if isinstance(name, Path):
            # If name is a Path object, the path should have the format: a/b/c/d.
            # However, in Windows, if we use `name = str(name)`, the `name` will be like 'a\\b\\c\\d'.
            # To avoid this, we use `name = name.as_posix()` to convert the Path object to string.
            name = name.as_posix()

        if self._is_path(name):
            return self.create_child(self._temp_path_list)

        if obj and not isinstance(obj, TreeNode):
            raise ValueError('TreeNode only add another TreeNode obj as child')
        if obj is None:
            obj = TreeNode(name)
        obj.parent = self
        self.child[name] = obj
        return obj

    def del_child(self, name):
        """remove a child node from current node"""
        if name in self.child:
            del self.child[name]

    def create_child(self, path):
        return self.find_child(path, create=True)

    @property
    def child_names(self):
        return list(self.child.keys())

    def has_more_children(self):
        return len(self.child) == 1

    def only_has_one_child(self):
        return len(self.child) == 1

    @property
    def first_child(self):
        return self.child[self.child_names[0]]

    def only_has_one_very_similar_child(self):
        # todo: cannot merge a file node and a folder node
        if len(self.child) != 1 or self.first_child.is_leaf_node:
            return False
        sim_level = string_similar(self.name, self.first_child.name)
        return sim_level > .6

    def del_me(self):
        father = self.parent
        if father is None:
            return None
        # print(leaf_node.path)
        father.del_child(self.name)
        if self.is_leaf_node:
            return father
            # return None
        # first_child = self.child[self.child_names[0]]
        # print(leaf_node.path)
        # todo: if we merge a child node to a parent node, we set the child node's name by the name of the parent node
        self.first_child.name = self.name
        father.add_child(self.first_child.name, self.first_child)
        # return first_child
        return father

    def del_first_child(self):
        first_child = self.first_child
        if first_child.is_leaf_node:
            return
        # print(leaf_node.path)

        self.child = first_child.child
        for child in self.child:
            self.child[child].parent = self
        # return self

    # def traverse_depth_first(self):
    #     yield self
    #     if self.is_leaf_node():
    #         return
    #     for x in self.child:
    #         next(self.traverse_depth_first(self.child[x]))

    @property
    def is_root_node(self):
        return self.parent is None

    @property
    def is_leaf_node(self):
        return len(self.child) == 0

    def _is_path(self, name):
        self._temp_path_list = get_path_list(name)
        if len(self._temp_path_list) == 1:
            return False
        return True

    def find_child(self, path, create=False):
        """find child node by path/name, return None if not found"""
        # convert path to a list if input is a string
        path = path if isinstance(path, list) else get_path_list(path)
        cur = self
        for sub in path:
            # search
            obj = cur.get_child(sub)
            if obj is None and create:
                # create new node if needed
                obj = cur.add_child(sub)
            # check if search done
            if obj is None:
                break
            cur = obj
        return obj

    def items(self):
        return self.child.items()

    def dump(self, indent=0):
        """dump tree to string"""
        tab = '   ' * (indent - 1) + '|- ' if indent > 0 else ''
        print('%s%s' % (tab, self.name))
        for name, obj in self.items():
            obj.dump(indent + 1)

    def prune_tree_from_top_to_down(self):
        """
        tree pruning: 树的剪枝算法
        """
        # self.dump()
        if self.is_leaf_node:
            return

        while self.only_has_one_very_similar_child():
            self.del_first_child()

        for child_name in self.child:
            self.child[child_name].prune_tree_from_top_to_down()
