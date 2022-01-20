from dataclasses import dataclass
from typing import Any, Type, Union, Callable
from copy import deepcopy

TypDanych = int

@dataclass
class BTNode:
    data: TypDanych
    left: Union[Type["BTNode"], None] = None
    right: Union[Type["BTNode"], None] = None
    
    __str__ = lambda self: str(self.data)
    __repr__ = lambda self: str(self.data)
    
@dataclass
class Node:
    data: TypDanych
    prev: Union[Type["Node"], None] = None

class Queue:
    lista: Node = None
    
    def put(self, dane: TypDanych) -> None:
        if self.lista:
            last = self._ostatnie()
            last.prev = Node(dane)
        else:
            self.lista = Node(dane)
    
    def pop(self) -> TypDanych:
        if self.lista:
            data = self.lista.data
            self.lista = self.lista.prev
            return data
        else:
            return None
    
    def _ostatnie(self) -> Node:
        last = self.lista
        while last.prev:
            last = last.prev
        return last

class Stack:
    lista: Node = None
    
    def put(self, dane: TypDanych) -> None:
        if self.lista:
            last = self._ostatnie()
            last.prev = Node(dane)
        else:
            self.lista = Node(dane)
    
    def pop(self) -> TypDanych:
        if self.lista:
            if self.lista.prev:
                last = self.lista
                while last.prev.prev:
                    last = last.prev
                data = last.prev.data
                last.prev = None
                return data

            else:
                data = self.lista.data
                self.lista = None
                return data
        else:
            return None
        
    def _ostatnie(self) -> Node:
        last = self.lista
        while last.prev:
            last = last.prev
        return last

root = BTNode(1)
root.left = BTNode(2)
root.right = BTNode(3)
root.left.left = BTNode(4)
root.left.right = BTNode(5)
root.right.left = BTNode(6)
root.right.right = BTNode(7)
#root.left.left.left = BTNode(8)
#root.left.left.right = BTNode(9)
#root.left.right.left = BTNode(10)
#root.left.right.right = BTNode(11)

prnt = lambda x: print(x, end=" ")

#1.1
def bt_wszerz(tree: BTNode, fn: Callable[[Any], None]) -> None:
    if tree:
        q = Queue()
        q.put(tree)
        while (node := q.pop()):
            fn(node)
            if node.left:
                q.put(node.left)
            if node.right:
                q.put(node.right)

#1.2
def bt_wzdluz(tree: BTNode, fn: Callable[[Any], None]) -> None:
    if tree:
        s = Stack()
        s.put(tree)
        while (node := s.pop()):
            fn(node)
            if node.right:
                s.put(node.right)
            if node.left:
                s.put(node.left)

bt_wszerz(root, prnt)
print()
bt_wzdluz(root, prnt)

warunek1 = lambda node: node.data == 2
warunek2 = lambda node: (node.left.data + node.right.data) >= 10

# nie było podane jak mamy zaimplementować więc zaimplementowałem dwa różne sposoby
# ¯\_(ツ)_/¯

def conditional_leaf_copy(tree: BTNode, warunek: Callable[[BTNode], bool]) -> BTNode:
    """kopiowanie na podstawie wybranego przez nas warunku wewnętrznego
    funkcja zaniechuje prace po pierwszym elemencie ze spełnionym warunkiem"""
    if tree:
        q = Queue()
        q.put(tree)
        while (node := q.pop()):
            if warunek(node):
                return deepcopy(node)
            if node.left:
                q.put(node.left)
            if node.right:
                q.put(node.right)
    

def order_leaf_copy(tree: BTNode, order: int) -> BTNode:
    """kopiowanie na podstawie kolejnosci w przechodzeniu po liscie w sposob
    preorder"""
    i = 1
    if tree:
        s = Stack()
        s.put(tree)
        while (node := s.pop()):
            if i == order:
                return deepcopy(node)
            if node.right:
                s.put(node.right)
            if node.left:
                s.put(node.left)
            i += 1

print()
print("right.data + left.data =>10: ", (_1 := conditional_leaf_copy(root, warunek2)))
bt_wszerz(_1, prnt)
print()
print("node.data = 2: ", (_2 := conditional_leaf_copy(root, warunek1)))
bt_wszerz(_2, prnt)
print()
print("order = 3: ", (_3 := order_leaf_copy(root, 3)))
bt_wszerz(_3, prnt)
print()
print("order = 6: ", (_4 := order_leaf_copy(root, 6)))
bt_wszerz(_4, prnt)
print()

#                       1
#                    /     \
# node.data == 2 => 2       3 <== left + right 
#                 /   \   /   \   ╚> 6+7 >=10
#                4     5 6     7
#    order == 3 ^^^     ^^^
#               order == 6

