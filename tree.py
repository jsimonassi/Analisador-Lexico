class Node:

    def __init__(self, name, children=[]):
        self.name = name
        self.children = children

    @staticmethod
    def make_node_by_recursive_list(recursive_list):
        result = []
        for i in range(0, len(recursive_list)):
            if i < len(recursive_list) - 1:
                new_node = Node(recursive_list[i], [recursive_list[i + 1]])
                if new_node not in result:
                    result.append(new_node)
            else:
                result.append(Node(recursive_list[i]))
        return result

    @staticmethod
    def append_child(tree, child):
        find = False
        for node in tree:
            if node.name == child.name:
                # Se o nó já está na lista, junta os filhos
                for child in child.children:
                    if child not in node.children:
                        node.children.append(child)
                find = True
                break

        if not find:  # Se o nó não está na lista, adiciona ele
            tree.append(child)

        return tree
