class Book:
    def __init__(self, title):
        self.header = Node(title)
        self.tail = self.header

    def add_line(self, line):
        new_node = Node(line)
        self.tail.next = new_node
        self.tail = new_node


class Node:
    def __init__(self, line):
        self.line = line
        self.next = None
        self.book_next = None


class SharedList:
    def __init__(self):
        self.header = None
        self.head = None
        self.last_book_tail = None

    def add_book(self, book):
        if not self.head:
            self.head = book.header
        else:
            self.last_book_tail.book_next = book.header
            self.last_book_tail.next = book.header
        self.last_book_tail = book.tail