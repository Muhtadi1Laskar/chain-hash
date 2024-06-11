import hashlib
import datetime
from merkle_root import calculate_markle_root


def hash_data(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


class Node:
    def __init__(self, value) -> None:
        self.timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.value = value
        self.hash = hash_data(value + self.timestamp)
        self.prev_hash = ""
        self.next = None


class Chain:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.length = 0

    def is_empty(self):
        return not self.head

    def append(self, value) -> None:
        if value == '':
            return 'Empty Inputs'
        
        new_node = Node(value)

        if self.is_empty():
            self.head = new_node
            self.head.prev_hash = None
            self.tail = self.head
            self.length += 1
            self.set_merkle_root()
            return

        previous_hash = self.tail.hash

        self.tail.next = new_node
        self.tail = new_node
        new_node.prev_hash = previous_hash
        self.length += 1
        self.set_merkle_root()

        return

    def log(self) -> list:
        li = []
        current_node = self.head

        while current_node:
            li.append((current_node.hash, current_node.prev_hash))
            current_node = current_node.next

        return li
    
    def get_block_data(self) -> None:
        if not self.head:
            return None
        
        li = []
        current_node = self.head

        while current_node:
            li.append(current_node.value)
            current_node = current_node.next
        return li
    
    def calculate_merkle_root(self):
        data = self.get_block_data()
        merkle_root, _ = calculate_markle_root(data)
        return merkle_root

    def set_merkle_root(self):
        root = self.calculate_merkle_root()
        self.head.merkle_root = root

    def html_format(self) -> None:
        if not self.head:
            return f"<center><h1>The chain is empty</h1></center>"
        
        html = []
        current_node = self.head

        while current_node:
            if self.head == current_node:
                html_text = f"""
                - Time Stamp: {current_node.timestamp}
                - Value: {current_node.value}
                - Hash: {current_node.hash}
                - Previous Hash: {current_node.prev_hash}
                - Merkle Root: {current_node.merkle_root}
            """
            else:    
                html_text = f"""
                - Time Stamp: {current_node.timestamp}
                - Value: {current_node.value}
                - Hash: {current_node.hash}
                - Previous Hash: {current_node.prev_hash}
                """

            html.append(html_text)
            current_node = current_node.next

        return html
    
    def empty_list(self):
        self.head = None
        self.tail = self.head
        self.length = 0
        return
    
    def get_merkle_data(self):
        if not self.head:
            return "The Chain is empty"
        
        data = self.get_block_data()
        _, tree_data = calculate_markle_root(data)
        return tree_data