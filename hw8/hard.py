def count_high_degree_nodes(graph):
    count = 0
    
    for node in graph.nodes():
        if graph.degree(node) > 5:
            count += 1
    
    return count


import networkx as nx

G = nx.Graph()
G.add_edges_from([
    (1,2), (1,3), (1,4), (1,5), (1,6), (1,7),
    (2,3), (2,4)
])

print(count_high_degree_nodes(G))
