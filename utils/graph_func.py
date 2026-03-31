import networkx as nx
from itertools import combinations


def all_biger_than2_cliques(G, max_size=None):
    """
    Yield all non-empty cliques of the undirected graph G.
    If max_size is given, only yield cliques with size <= max_size.
    """
    for clique in nx.find_cliques(G):  # maximal cliques
        n = len(clique)
        # Determine sizes to generate
        sizes = range(3, n+1) if max_size is None else range(3, min(max_size, n)+1)
        for k in sizes:
            for sub in combinations(clique, k):
                yield tuple(sub)
