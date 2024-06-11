import hashlib

class Node:
    def __init__(self, left, right, value, content, is_copied=False):
        self.left = left
        self.right = right
        self.value = value
        self.content = content
        self.is_copied = is_copied
    
    def hash(value):
        return hashlib.sha256(value.encode('utf-8')).hexdigest()
    
    def __str__(self):
        return str(self.value)
    
    def copy(self):
        return Node(self.right, self.left, self.value, self.content, True)


class MerkleTree:
    def __init__(self, values):
        self.__buildTree(values)
    
    def __buildTree(self, values):
        leaves = [Node(None, None, Node.hash(e), e) for e in values]

        if len(leaves) % 2 != 0:
            leaves.append(leaves[-1].copy())
        
        self.root = self.__buildTreeRec(leaves)
    
    def __buildTreeRec(self, nodes):
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1].copy())
        
        half = len(nodes) // 2

        if len(nodes) == 2:
            value = Node.hash(nodes[0].value + nodes[1].value)
            content = f"{nodes[0].content} + {nodes[1].content}"
            return Node(nodes[0], nodes[1], value, content)
        
        left = self.__buildTreeRec(nodes[:half])
        right = self.__buildTreeRec(nodes[half:])
        values = Node.hash(left.value + right.value)
        content = f"{left.content} + {right.content}"

        return Node(left, right, values, content)

    def get_nodes_up_to_root(self):
        nodes = []
        self.__collect_nodes(self.root, nodes)
        return nodes

    def __collect_nodes(self, node: Node, nodes) -> None:
        if node is not None:
            nodes.append({
                "value": node.value,
                "content": node.content,
            })
            self.__collect_nodes(node.left, nodes)
            self.__collect_nodes(node.right, nodes)

    def get_root(self):
        return self.root

def calculate_markle_root(value):
    markle_tree = MerkleTree(value)
    root = markle_tree.get_root()
    data = markle_tree.get_nodes_up_to_root()

    return [root, data]
