from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any


class Color(Enum):
    RED = 0
    BLACK = 1


@dataclass
class Node:
    value: Any
    left: Optional[Node]
    right: Optional[Node]
    parent: Optional[Node]
    color: Color

    @staticmethod
    def new_black(value):
        return Node(value, None, None, None, Color.BLACK)

    @staticmethod
    def new_red(value):
        return Node(value, None, None, None, Color.RED)

    def insert_child(self, value) -> Node:
        if value < self.value:
            if self.left is None:
                self.left = Node.new_red(value)
                self.left.parent = self
                return self.left
            else:
                return self.left.insert_child(value)
        else:
            if self.right is None:
                self.right = Node.new_red(value)
                self.right.parent = self
                return self.right
            else:
                return self.right.insert_child(value)

    def get_uncle(self) -> Node | None:
        if self.parent is None or self.parent.parent is None:
            return None

        grandparent = self.parent.parent
        if grandparent.left == self.parent:
            return grandparent.right
        else:
            return grandparent.left

    def rotate_left(self):
        if self.right is None:
            return

        if self.parent:
            if self.parent.right == self:
                self.parent.right = self.right
            else:
                self.parent.left = self.right

        self.right.parent = self.parent
        self.parent = self.right

        self.right.left, self.right = self, self.right.left
        if self.right:
            self.right.parent = self

    def rotate_right(self):
        if self.left is None:
            return

        if self.parent:
            if self.parent.right == self:
                self.parent.right = self.left
            else:
                self.parent.left = self.left

        self.left.parent = self.parent
        self.parent = self.left

        self.left.right, self.left = self, self.left.right
        if self.left:
            self.left.parent = self

    def height(self):
        left_height = self.left.height() if self.left else 0
        right_height = self.right.height() if self.right else 0

        return max(left_height, right_height) + 1

    def find(self, value) -> Node | None:
        if self.value == value:
            return self
        elif value < self.value:
            return self.left.find(value) if self.left else None
        else:
            return self.right.find(value) if self.right else None


class RbTree:
    root: Optional[Node]

    def __init__(self):
        self.root = None

    def height(self) -> int:
        return self.root.height() if self.root else 0

    def find(self, value) -> Node | None:
        return self.root.find(value) if self.root else None

    def insert(self, value):
        if self.root is None:
            self.root = Node.new_black(value)
            return
        inserted_node = self.root.insert_child(value)
        self.insert_fixup(inserted_node)

    def insert_fixup(self, node: Node):
        # case 1: node is root -> set to black
        if node.parent is None:
            node.color = Color.BLACK
            return

        parent = node.parent

        # case 2: parent is black -> do nothing
        if parent.color == Color.BLACK:
            return

        # case 3: parent is root
        if parent.parent is None:
            node.parent.color = Color.BLACK
            return

        grandparent = parent.parent
        uncle = node.get_uncle()

        # parent is red and not root

        # case 3: uncle is red -> recolor then fixup grandparent
        if uncle and uncle.color == Color.RED:
            parent.color = Color.BLACK
            uncle.color = Color.BLACK
            grandparent.color = Color.RED
            self.insert_fixup(grandparent)
            return

        # uncle is black

        # case 4: node is inner child -> rotate with parent
        if grandparent.left == parent and parent.right == node:
            parent.rotate_left()
            node, parent = parent, node
        elif grandparent.right == parent and parent.left == node:
            parent.rotate_right()
            node, parent = parent, node

        # case 5: node is outer child -> rotate so parent becomes grandparent
        grandparent.color = Color.RED
        parent.color = Color.BLACK

        if grandparent.left == parent:
            grandparent.rotate_right()
        else:
            grandparent.rotate_left()

        if grandparent == self.root:
            self.root = parent


def main():
    tree = RbTree()
    for i in range(1, 11):
        tree.insert(i)

    print(tree.height())


if __name__ == '__main__':
    main()