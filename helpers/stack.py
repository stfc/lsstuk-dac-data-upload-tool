# Bradley N. Miller, David L. Ranum
# Introduction to Data Structures and Algorithms in Python
# Copyright 2005
#
# stack.py

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    # MS addition
    def pop_many(self, number_of_items):
        to_return: list = []
        for i in range(0, number_of_items):
            try:
                to_return.append(self.items.pop())
            except IndexError:
                break
        return to_return
