""" if __name__ == "__main__":
    print("MATIRX")
    nodes, adj_matrix = csv_to_matrix('smallworld2.csv')

    graph = Graph(adj_matrix, nodes)
    k, n = graph.propagate(NodesInKnowledgePropagation(nodes))

    print(k, n)
"""