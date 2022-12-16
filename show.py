import networkx as nx
from pyvis.network import Network


def show_derivation_tree(derivation_tree):
    net = Network()
    graph = nx.DiGraph()

    for node in derivation_tree:
        graph.add_node(node.name)
        for child in node.children:
            graph.add_node(child)
            graph.add_edge(node.name, child)

    net.from_nx(graph)
    net.show("derivation_tree.html")
