from typing import Optional


class Node:
    """
    Class representing a single node of a binary tree containing integer values.

    ...

    Attributes
    ----------

    value: int
        Value stored in the node.
    parent: Node, optional
        Parent of the current node. Can be None.
    left: Node, optional
        Left child of the current node. Can be None.
    right: Node, optional
        Right child of the current node. Can be None.
    """
    def __init__(self, value: int) -> None:
        self.value = value
        self.parent = self.right = self.left = None

    def set_left_child(self, node: Optional['Node']) -> None:
        """
        Set the the left child of self to the given node.
        Sets the node's parent to self (if it is not None).

        Args:
            node (Node, optional): the node to set as the child.
        """
        self.left = node
        if node is not None:
            node.parent = self

    def set_right_child(self, node: Optional['Node']) -> None:
        """
        Set the the right child of self to the given node.
        Sets the node's parent to self (if it is not None).

        Args:
            node (Node, optional): the node to set as the child.
        """
        self.right = node
        if node is not None:
            node.parent = self

def right_rotation(node: Node, root: Node) -> Node:
    """Right rotate a node

    Do a right rotation on the node specified as the first argument and return the root
    of the tree. The root can be the specified, second arugment (root) or a new root which
    changed because of the rotation.

    Args:
        node (Node): The node on which the rotation is done.
        root (Node): Root node of the binary tree which contains the node which we are rotating.

    Returns:
        Node: The root of the binary tree, which could have changed due to the rotation.
    """
    rotator = node.left
    new_root = root
    if rotator is None:
        return new_root
    parent = node.parent
    if parent is None:
        new_root = rotator
        new_root.parent = None
    else:
      if parent.left == rotator:
        parent.set_left_child(rotator)
      if parent.right == rotator:
        parent.set_right_child(rotator)

    temp = rotator.right
    rotator.set_right_child(node)
    node.set_left_child(temp)

    return new_root

def print_tree(node: Optional[Node], level: int = 0) -> None:
    """
    Prints a rough sketch of the tree in the command line.

    Accepts a node which can be None and prints its right subtree, than its value and then its left subtree, recursivevly.

    Args:
        node (Node, optional): The node for which we are writing out the subtree.
        level (int): Number of empty lines before the actual value - used to discern the tree levels.
    """
    if node is None:
        return
    print_tree(node.right, level + 4)
    print(' ' * level + f'-> {node.value}')
    print_tree(node.left, level + 4)


root = Node(17)
root.set_left_child(Node(13))
root.left.set_left_child(Node(10))
root.left.set_right_child(Node(12))
root.left.set_right_child(Node(15))
root.left.right.set_left_child(Node(14))
root.set_right_child(Node(20))
root.right.set_left_child(Node(19))
root.right.set_right_child(Node(22))
root.right.left.set_left_child(Node(18))

# root = Node('A')
# rootLeft = Node('B')
# root.set_left_child(rootLeft)

# #B
# root.left.set_left_child(Node('C'))
# root.left.set_right_child(Node('Br'))

# #C
# root.left.left.set_left_child(Node('Cl'))
# root.left.left.set_right_child(Node('Cr'))

print('Prije rotacije:')
print_tree(root)

# Right rotate around the root (first argument)
root = right_rotation(root, root)

print(root.value)

assert root.value == 13
assert root.left.value == 10
assert root.right.value == 17
assert root.right.left.value == 15
assert root.right.left.left.value == 14
assert root.right.right.value == 20
assert root.right.right.left.value == 19
assert root.right.right.left.left.value == 18
assert root.right.right.right.value == 22

print()
print('Nakon rotacije:')
print_tree(root)
