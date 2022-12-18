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
    def append_child(tree, child, tree_items):
        if not tree:  # Se árvore está vazia, inicializa com o primeiro ramo
            for node in child:
                tree.append(node)
                tree_items.append(node.name)
            return tree, tree_items

        last_father_index = 0
        for i in range(0, len(tree)):
            if tree[i].name == child[i].name:
                last_father_index = i
            else:
                break

        new_node_name = Node.get_new_node_name(child[last_father_index + 1].name, tree_items)
        tree[last_father_index].children.append(new_node_name)
        tree_items.append(new_node_name)
        for i in range(last_father_index + 1, len(child)):
            child[i].name = Node.get_new_node_name(child[i].name, tree_items)
            tree_items.append(child[i].name)
            for j in range(0, len(child[i].children)):
                child[i].children[j] = Node.get_new_node_name(child[i].children[j], tree_items)
                tree_items.append(child[i].children[j])
            tree.append(child[i])

        return tree, tree_items

    def __eq__(self, other):
        filterd_self = self.name.replace("*", "")
        filterd_other = other.name.replace("*", "")
        return filterd_self == filterd_other

    @staticmethod
    def get_new_node_name(node_name, node_list):
        acc = 0
        for name in node_list:
            if name == node_name:
                acc += 1
        if acc >= 2:
            return node_name + "*"
        return node_name
