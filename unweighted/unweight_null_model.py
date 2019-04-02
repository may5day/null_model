# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 20:42:23 2017
revised on Oct 15 2017
@author:xiaoke
"""

import networkx as nx
import random
import copy


__all__ = ['judge_error'
           'count_degree_nodes',  # dict_degree_nodes
           'er_graph',  # ER_model
           'config_model',
           'random_0k',
           'random_1k',
           'random_2k',
           'random_25k',
           'random_3k',
           'rich_club_create',
           'rich_club_break',
           'assort_mixing',
           'disassort_mixing',
           'random_1kd']


def judge_error(G, n_swap, max_tries, connected):
    if not nx.is_connected(G):
        raise nx.NetworkXError("For connected graphs only.")
    if G.is_directed():
        raise nx.NetworkXError("For undirected graphs only.")
    if n_swap > max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G) < 3:
        raise nx.NetworkXError("This graph has less than three nodes.")


def count_degree_nodes(degree_nodes):
    """Count nodes with the same degree

    Parameters
    ----------
    degree_nodes : list
        a list contains nodes and degree [[degree,node]]

    Returns
    -------
    a dict contains nodes and degree {degree:[node1,node2...]}
    where node1 and node2 have the same degree

    Examples
    --------
    >>> from unweighted_null_model import count_degree_node
    >>> n_list = [[1,2],[1,3],[2,4],[2,5]]
    >>> count_degree_node(n_list)
    ... {1: [2, 3], 2: [4, 5]}s
    """
    degree_dict = {}
    for dn_i in degree_nodes:
        if dn_i[0] not in degree_dict:
            degree_dict[dn_i[0]] = [dn_i[1]]
        else:
            degree_dict[dn_i[0]].append(dn_i[1])
    return degree_dict


def er_graph(G):
    """Returns a random graph G_{n,p} (Erdős-Rényi graph, binomial graph).

    Chooses each of the possible edges with probability p.

    Parameters
    ----------
    G : undirected and unweighted graph
    n : int
        The number of nodes.
    p : float
        Probability for edge creation.
    directed : bool, optional (default=False)
        If True return a directed graph

    Notes
    -----
    The G_{n,p} graph algorithm chooses each of the [n(n-1)]/2
    (undirected) or n(n-1) (directed) possible edges with probability p.

    References
    ----------
    .. [1] P. Erdős and A. Rényi, On Random Graphs, Publ. Math. 6, 290 (1959).
    .. [2] E. N. Gilbert, Random Graphs, Ann. Math. Stat., 30, 1141 (1959).
    """
    n = len(G.nodes())
    m = len(G.edges())
    p = 2.0 * m / (n * n)
    return nx.random_graphs.erdos_renyi_graph(n, p, directed=False)


def config_model(G):
    """Returns a random bipartite graph from the given graph

    Parameters
    ----------
    G : undirected and unweighted graph
    degree_seq : list
        Degree sequence of the given graph G
    """
    degree_seq = list(G.degree().values())
    return nx.configuration_model(degree_seq)


def random_0k(G, n_swap=1, max_tries=100, connected=1):
    """Returns a 0K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : undirected and unweighted graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    The 0K null models have the same average node degree as the original graph

    See Also
    --------
    er_graph

    """
    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0
    edges = G.edges()
    nodes = G.nodes()
    while swapcount < n_swap:
        n_try = n_try + 1
        # choose a edge randomly
        u, v = random.choice(edges)
        # choose two nodes which are not connected
        x, y = random.sample(nodes, 2)
        if len(set([u, v, x, y])) < 4:
            continue
        if (x, y) not in edges and (y, x) not in edges:
            # cut the original edge
            G.remove_edge(u, v)
            # connect the new edge
            G.add_edge(x, y)
            edges.remove((u, v))
            edges.append((x, y))

            # if connected = 1 but the original graph is not connected fully,
            # withdraw the operation about the swap of edges.
            if connected == 1:
                if not nx.is_connected(G):
                    G.add_edge(u, v)
                    G.add_edge(x, y)
                    G.remove_edge(u, y)
                    G.remove_edge(x, v)
                    continue
            swapcount += 1

        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                 n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
    return G


def random_1k(G, n_swap=1, max_tries=100, connected=1):
    """Returns a 1K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : undirected and unweighted graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    The 1K null models require reproducing the original graph’s
    node degree distribution.

    """

    judge_error(G, n_swap, max_tries, connected)

    n_try = 0
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                 n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges
        # (u-v,x-y) randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # make sure the four nodes are not repeated
        if len(set([u, v, x, y])) == 4:
            # make sure the new edges are not exist in the original graph
            if (y not in G[u]) and (v not in G[x]):
                # add two new edges
                G.add_edge(u, y)
                G.add_edge(v, x)
                # delete two old edges
                G.remove_edge(u, v)
                G.remove_edge(x, y)
                # if connected = 1 but the original graph is not connected fully,
                # withdraw the operation about the swap of edges.
                if connected == 1:
                    if not nx.is_connected(G):
                        G.add_edge(u, v)
                        G.add_edge(x, y)
                        G.remove_edge(u, y)
                        G.remove_edge(x, v)
                        continue
                swapcount += 1
    return G


def random_2k(G, n_swap=1, max_tries=100, connected=1):
    """Returns a 2K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : undirected and unweighted graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    The 2K null models have the same joint degree distribution as the original graph

    """
    # make sure the 2K-characteristic unchanged and the graph is connected
    # swap the edges inside the community
    judge_error(G, n_swap, max_tries, connected)
    n_try = 0
    swapcount = 0
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                 n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1

        # make sure the degree distribution unchanged,choose two edges (u-v,x-y) randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        # make sure the four nodes are not repeated
        if len(set([u, v, x, y])) == 4:
            # make sure the degree matching characteristic of the nodes remain unchanged
            if G.degree(v) == G.degree(y): 
                # make sure the new edges are not exist in the original graph
                if (y not in G[u]) and (v not in G[x]):
                	# add two new edges
                    G.add_edge(u, y)
                    G.add_edge(v, x)
                    # delete two old edges
                    G.remove_edge(u, v)
                    G.remove_edge(x, y)
                    # if connected = 1 but the original graph is not connected fully,
                    # withdraw the operation about the swap of edges.
                    if connected == 1:
                        if not nx.is_connected(G):
                            G.add_edge(u, v)
                            G.add_edge(x, y)
                            G.remove_edge(u, y)
                            G.remove_edge(x, v)
                            continue
                    swapcount += 1
    return G


def random_25k(G, n_swap=1, max_tries=100, connected=1):
    """Returns a 2.5K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : undirected and unweighted graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    The 2.5K null models has the same clustering spectrum and joint degree distribution with the original network

    """
    # make sure the 2K-characteristic unchanged and the graph is connected
    # swap the edges inside the community
    judge_error(G, n_swap, max_tries, connected)

    n_try = 0
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                 n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1

        # make sure the degree distribution unchanged,choose two edges (u-v,x-y) randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # make sure the four nodes are not repeated
        if len(set([u, v, x, y])) == 4:
            # make sure the degree matching characteristic of the nodes remain unchanged
            if G.degree(v) == G.degree(y):
                # make sure the new edges are not exist in the original graph
                if (y not in G[u]) and (v not in G[x]):
                    G.add_edge(u, y)
                    G.add_edge(v, x)

                    G.remove_edge(u, v)
                    G.remove_edge(x, y)
                    # get the degree of four nodes and their neighbor nodes, degree_node_list : [[degree,node]]
                    degree_node_list = map(lambda t: (t[1], t[0]), G.degree(
                        [u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])).items())
                    # get all nodes of each degree :{degree:[node1,node2...]}
                    dict_degree = count_degree_nodes(degree_node_list)

                    for i in range(len(dict_degree)):
                        avcG = nx.average_clustering(
                            G, nodes=dict_degree.values()[i], weight=None, count_zeros=True)
                        avcG = nx.average_clustering(
                            G, nodes=dict_degree.values()[i], weight=None, count_zeros=True)
                        i += 1
                    # if the clustering coefficient about dgree changed after scrambling ,withdraw this operation
                    if avcG != avcG:
                        G.add_edge(u, v)
                        G.add_edge(x, y)
                        G.remove_edge(u, y)
                        G.remove_edge(x, v)
                        break
                    # if connected = 1 but the original graph is not connected fully,
                    # withdraw the operation about the swap of edges.
                    if connected == 1:
                        if not nx.is_connected(G):
                            G.add_edge(u, v)
                            G.add_edge(x, y)
                            G.remove_edge(u, y)
                            G.remove_edge(x, v)
                            continue

                    swapcount += 1
    return G


def random_3k(G, n_swap=1, max_tries=100, connected=1):
    """Returns a 3K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : undirected and unweighted graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    3K null model, which is considered interconnectivity among triples of nodes

    """

    # make sure the 2K-characteristic unchanged and the graph is connected
    # swap the edges inside the community
    judge_error(G, n_swap, max_tries, connected)

    n_try = 0
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                 n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1

        # make sure the degree distribution unchanged,choose two edges (u-v,x-y) randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # make sure the four nodes are not repeated
        if len(set([u, v, x, y])) == 4:
            # make sure the degree matching characteristic of the nodes remain unchanged
            if G.degree(v) == G.degree(y):
                # make sure the new edges are not exist in the original graph
                if (y not in G[u]) and (v not in G[x]):
                    G.add_edge(u, y)
                    G.add_edge(v, x)

                    G.remove_edge(u, v)
                    G.remove_edge(x, y)

                    # get the set of four nodes and their neighbor nodes
                    node_list = [u, v, x, y] + \
                        list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])
                    # cal the clustering coefficient of the four nodes in the original and the new graph
                    avcG = nx.clustering(G, nodes=node_list)
                    avcG = nx.clustering(G, nodes=node_list)
                    # if the clustering coefficient about dgree changed after scrambling ,withdraw this operation
                    if avcG != avcG:
                        G.add_edge(u, v)
                        G.add_edge(x, y)
                        G.remove_edge(u, y)
                        G.remove_edge(x, v)
                        continue
                    # if connected = 1 but the original graph is not connected fully,
                    # withdraw the operation about the swap of edges.
                    if connected == 1:
                        if not nx.is_connected(G):
                            G.add_edge(u, v)
                            G.add_edge(x, y)
                            G.remove_edge(u, y)
                            G.remove_edge(x, v)
                            continue
                    swapcount += 1
    return G


def rich_club_create(G, k=1, n_swap=1, max_tries=100, connected=1): 
    """Returns a null model where the rich-club connectivity is preserved.
    
    choose two edges between hubs and non-hubs randomly, if there is no edge between hubs and between non-hubs,
    reconnect links until the times you try reached the max_tries or there are edges between all hubs.

    Parameters
    ----------
    G : undirected and unweighted graph
    k : int
        threshold value of the degree of hubs
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    hub_edges : the edges between hubs
    nonhub_edges : the edges between non-hubs

    """

    judge_error(G, n_swap, max_tries, connected)

    n_try = 0
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    # all hubs
    hubs = [e for e in G.nodes() if G.degree()[e] >= k]
    # the edges between hubs that exist in original graph
    hubs_edges = [e for e in G.edges() if G.degree()[e[0]] >= k and G.degree()[
        e[1]] >= k]
    # the number of edges between all hubs
    len_possible_edges = len(hubs) * (len(hubs) - 1) / 2

    while swapcount < n_swap and len(hubs_edges) < len_possible_edges:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                 n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
        #  choose two hubs randomly
        u, y = random.sample(hubs, 2)
        v = random.choice(list(G[u]))
        x = random.choice(list(G[y]))
        if len(set([u, v, x, y])) == 4:
            # the other node is not a hub
            if G.degree()[v] > k or G.degree()[x] > k:
                continue
        # make sure the new edges are not exist in the original graph
        if (y not in G[u]) and (v not in G[x]):
            G.add_edge(u, y)
            G.add_edge(x, v)

            G.remove_edge(u, v)
            G.remove_edge(x, y)
            # update edges between hubs
            hubs_edges.append((u, y))
            # if connected = 1 but the original graph is not connected fully,
            # withdraw the operation about the swap of edges.
            if connected == 1:
                if not nx.is_connected(G):
                    G.add_edge(u, v)
                    G.add_edge(x, y)

                    G.remove_edge(u, y)
                    G.remove_edge(x, v)
                    hubs_edges.remove((u, y))
                    continue

        if n_try >= max_tries:
            print('Maximum number of attempts (%s) exceeded ' % n_try)
            break
        swapcount += 1
    return G


def rich_club_break(G, k=10, n_swap=1, max_tries=100, connected=1):
    """Returns a null model where the rich-club connectivity is not preserved.
    
    choose two edges between hubs and non-hubs randomly, if there is no edge between hubs and non-hubs,
    reconnect links until the times you try reached the max_tries or there are no hub edges or non-hub edges.

    Parameters
    ----------
    G : undirected and unweighted graph
    k : int
        threshold value of the degree of hubs
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    hub_edges : the edges between hubs
    nonhub_edges : the edges between non-hubs

    """

    judge_error(G, n_swap, max_tries, connected)

    n_try = 0
    swapcount = 0

    hubs_edges = []
    nonhub_edges = []
    # all hubs
    hubs = [e for e in G.nodes() if G.degree()[e] > k]
    for e in G.edges():
        if e[0] in hubs and e[1] in hubs:
            hubs_edges.append(e)
        elif e[0] not in hubs and e[1] not in hubs:
            nonhub_edges.append(e)

    swapcount = 0
    while swapcount < n_swap and hubs_edges and nonhub_edges:
        # choose two edges(hub and non-hub) randomly
        u, v = random.choice(hubs_edges)
        x, y = random.choice(nonhub_edges)
        if len(set([u, v, x, y])) < 4:
            continue
        # make sure the new edges are not exist in the original graph
        if (y not in G[u]) and (v not in G[x]):
            G.add_edge(u, y)
            G.add_edge(x, v)
            G.remove_edge(u, v)
            G.remove_edge(x, y)
            hubs_edges.remove((u, v))
            nonhub_edges.remove((x, y))
            # if connected = 1 but the original graph is not connected fully,
            # withdraw the operation about the swap of edges.
            if connected == 1:
                if not nx.is_connected(G):
                    G.add_edge(u, v)
                    G.add_edge(x, y)
                    G.remove_edge(u, y)
                    G.remove_edge(x, v)
                    hubs_edges.append((u, v))
                    nonhub_edges.append((x, y))
                    continue
        if n_try >= max_tries:
            print('Maximum number of attempts (%s) exceeded ' % n_try)
            break
        swapcount += 1
    return G


def assort_mixing(G, k=10, n_swap=1, max_tries=100, connected=1):
    """Returns a assortative graph

    choose two edges (four nodes) randomly, sort these nodes by degree,
    connect the first two nodes and the last nodes separately.

    Parameters
    ----------
    G : undirected and unweighted graph
    k : int
        threshold value of the degree of hubs
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    """

    judge_error(G, n_swap, max_tries, connected)

    n_try = 0
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        n_try += 1

        # make sure the degree distribution unchanged,choose two edges (u-v,x-y) randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) < 4:
            continue
        sortednodes = zip(
            *sorted(G.degree([u, v, x, y]).items(), key=lambda d: d[1], reverse=True))[0]
        if (sortednodes[0] not in G[sortednodes[1]]) and (sortednodes[2] not in G[sortednodes[3]]):
            # make sure the new edges are not exist in the original graph

            G.add_edge(sortednodes[0], sortednodes[1])
            G.add_edge(sortednodes[2], sortednodes[3])
            G.remove_edge(x, y)
            G.remove_edge(u, v)

            if connected == 1:
                if not nx.is_connected(G):
                    G.remove_edge(sortednodes[0], sortednodes[1])
                    G.remove_edge(sortednodes[2], sortednodes[3])
                    G.add_edge(x, y)
                    G.add_edge(u, v)
                    continue
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                 n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        swapcount += 1
    return G


def disassort_mixing(G, k=10, n_swap=1, max_tries=100, connected=1):
    """Returns a disassortative graph

    choose two edges (four nodes) randomly, sort these nodes by degree,
    connect the first and the last nodes as well as the second and the third nodes separately.

    Parameters
    ----------
    G : undirected and unweighted graph
    k : int
        threshold value of the degree of hubs
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----

    """

    judge_error(G, n_swap, max_tries, connected)

    n_try = 0
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        n_try += 1

        # make sure the degree distribution unchanged,choose two edges (u-v,x-y) randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) < 4:
            continue
        sortednodes = zip(
            *sorted(G.degree([u, v, x, y]).items(), key=lambda d: d[1], reverse=True))[0]
        if (sortednodes[0] not in G[sortednodes[3]]) and (sortednodes[1] not in G[sortednodes[2]]):
            # make sure the new edges are not exist in the original graph

            G.add_edge(sortednodes[0], sortednodes[3])
            G.add_edge(sortednodes[1], sortednodes[2])
            G.remove_edge(x, y)
            G.remove_edge(u, v)

            if connected == 1:
                if not nx.is_connected(G):
                    G.remove_edge(sortednodes[0], sortednodes[3])
                    G.remove_edge(sortednodes[1], sortednodes[2])
                    G.add_edge(x, y)
                    G.add_edge(u, v)
                    continue
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                 n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        swapcount += 1
    return G


# to be connected...
def random_1kd(G, n_swap=1, max_tries=100):
    """Returns a 1K null model beased on random reconnection algorithm

    choose two edges (u->v and x->y), if u->y and x->v don't exist ,reconnect these edges.
    Parameters
    ----------
    G : directed and unweighted graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    """
    if not G.is_directed():
        raise nx.NetworkXError("For directed graphs only.")
    if n_swap > max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G) < 4:
        raise nx.NetworkXError("This graph has less than four nodes.")
    n_try = 0
    swapcount = 0
    while swapcount < n_swap:
        (u, v), (x, y) = random.sample(G.edges(), 2)
        if len(set([u, v, x, y])) < 4:
            continue
        # reconnection
        if (x, v) not in G.edges() and (u, y) not in G.edges():
            G.add_edge(u, y)
            G.add_edge(x, v)
            G.remove_edge(u, v)
            G.remove_edge(x, y)
            swapcount += 1
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                 n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
    return G
