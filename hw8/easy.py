def count_nodes(graph):
    return graph.number_of_nodes()



import networkx as nx

G = nx.Graph()
G.add_edges_from([
    (1,2), (1,3), (1,4), (1,5), (1,6), (1,7),
    (2,3), (2,4)
])

print(count_nodes(G))


"""
GPT Promt: Can create some sample data for this code:
def count_nodes(graph):
    return graph.number_of_nodes()

"""