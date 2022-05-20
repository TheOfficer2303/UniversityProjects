class Tree:
    def __init__(self, branch_list):
        self.branch_list = branch_list


class Node:
    def __init__(self, value, tree: Tree):
        self.value = value
        self.tree = tree


class Leaf:
    def __init__(self, value):
        self.value = value
