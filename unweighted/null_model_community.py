# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 20:42:23 2017
revised on Oct 15 2017
@author: Aipan1
"""

import networkx as nx
import random
import copy


__all__ = ['judge_error'
           'edge_in_community',
           'count_degree_nodes',
           'inner_random_1k',
           'inner_random_2k',
           'inner_random_25k',
           'inner_random_3k',
           'inter_random_1k',
           'inter_random_2k',
           'inter_random_25k',
           'inter_random_3k',
           'inner_community_swap',
           'inter_community_swap',
           'Q_enhense',
           'Q_weaken', ]


def judge_error(G, n_swap, max_tries, connected):
    if not nx.is_connected(G):
        raise nx.NetworkXError("For connected graphs only.")
    if G.is_directed():
        raise nx.NetworkXError("For undirected graphs only.")
    if n_swap > max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G) < 3:
        raise nx.NetworkXError("This graph has less than three nodes.")


def edge_in_community(node_community, edge):
    """Returns True if the edge is in the community, false otherwise.

    Parameters
    ----------
    node_community : list
        nodes and the communities they belong to
    edge:
        an edge in the graph`12

    Notes
    -----

    Examples
    --------
    """
    return_value = 0
    for nc_i in node_community:
        if edge[0] in nc_i and edge[1] in nc_i:
            return_value += 1
    if return_value == 0:
        return 0
    else:
        return 1


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
    """
    degree_dict = {}
    for dni in degree_nodes:
        if dni[0] not in degree_dict:
            degree_dict[dni[0]] = [dni[1]]
        else:
            degree_dict[dni[0]].append(dni[1])
    return degree_dict


def inner_random_1k(G, node_community, n_swap=1, max_tries=100, connected=1):
    """Returns a 1K null model beased on random reconnection algorithm inner community

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the degree distribution unchanged and the graph connected.
    Swap edges inner communities.

    """
    judge_error(G, n_swap, max_tries, connected)
    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly.
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inner community.
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:
                # Make sure the edges created are inner community.
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:
                    # Make sure the new edges are not exist in the original
                    # graph.
                    if (y not in G[u]) and (v not in G[x]):
                        G.add_edge(u, y)
                        G.add_edge(v, x)

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


def inner_random_2k(G, node_community, n_swap=1, max_tries=100, connected=1):
    """Returns a 2K null model beased on random reconnection algorithm inner community

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 2k-characteristic unchanged and the graph connected.
    Swap edges inner communities.

    """
    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly.
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inner community.
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:
                # Make sure the edges created are inner community.
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:
                    # Keep the degree matching characteristic of nodes
                    # unchanged.
                    if G.degree(v) == G.degree(y):
                        # Make sure the new edges are not exist in the original
                        # graph.
                        if (y not in G[u]) and (v not in G[x]):
                            G.add_edge(u, y)
                            G.add_edge(v, x)

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


def inner_random_25k(G, node_community, n_swap=1, max_tries=100, connected=1):
    """Returns a 2.5K null model beased on random reconnection algorithm inner community

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 2.5k-characteristic unchanged and the graph connected.
    Swap edges inner communities.

    """
    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inner community.
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:
                # Make sure the edges created are inner community.
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:
                    # Keep the degree matching characteristic of nodes
                    # unchanged.
                    if G.degree(v) == G.degree(y):
                        # Make sure the new edges are not exist in the original
                        # graph.
                        if (y not in G[u]) and (v not in G[x]):
                            G.add_edge(u, y)
                            G.add_edge(v, x)

                            G.remove_edge(u, v)
                            G.remove_edge(x, y)

                            degree_node_list = map(lambda t: (t[1], t[0]), G.degree(
                                [u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])).items())

                            D = count_degree_nodes(degree_node_list)
                            for i in range(len(D)):
                                avcG = nx.average_clustering(
                                    G, nodes=D.values()[i], weight=None, count_zeros=True)
                                avcG = nx.average_clustering(
                                    G, nodes=D.values()[i], weight=None, count_zeros=True)
                                i += 1
                                # If the degree-related clustering coefficient changed after scrambling
                                # withdraw this operation about scrambling.
                                if avcG != avcG:
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    break
                                # if connected = 1 but the original graph is not connected fully,
                                # withdraw the operation about the swap of
                                # edges.
                                if connected == 1:
                                    if not nx.is_connected(G):
                                        G.add_edge(u, v)
                                        G.add_edge(x, y)
                                        G.remove_edge(u, y)
                                        G.remove_edge(x, v)
                                        continue
                                swapcount += 1

    return G


def inner_random_3k(G, node_community, n_swap=1, max_tries=100, connected=1):
    """Returns a 3K null model beased on random reconnection algorithm inner community

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 3k-characteristic unchanged and the graph connected.
    Swap edges inner communities.

    """
    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inter communities.
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:
                # Make sure the edges created are inner community.
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:
                    # Keep the degree matching characteristic of nodes
                    # unchanged.
                    if G.degree(v) == G.degree(y):

                        # Make sure the new edges are not exist in the original
                        # graph.
                        if (y not in G[u]) and (v not in G[x]):
                            G.add_edge(u, y)
                            G.add_edge(v, x)

                            G.remove_edge(u, v)
                            G.remove_edge(x, y)
                            # Get the set of four nodes and their neighbor
                            # nodes.
                            node_list = [
                                u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])
                            # Calculate the clustering coefficient of all these
                            # nodes in the original graph and the new graph.
                            avcG = nx.clustering(G, nodes=node_list)
                            avcG = nx.clustering(G, nodes=node_list)
                            # Keep the clustering coefficient of four nodes equal.
                            # Withdraw the operation about the swap of edges,
                            # otherwise.
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


def inter_random_1k(G, node_community, n_swap=1, max_tries=100, connected=1):
    """Returns a 1K null model beased on random reconnection algorithm inter communities

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the degree distribution unchanged and the graph connected.
    Swap edges inter communities.

    """
    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated.
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inner community.
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:
                # Make sure the edges created are inner community.
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:

                    # Make sure the new edges are not exist in the original
                    # graph.
                    if (y not in G[u]) and (v not in G[x]):
                        G.add_edge(u, y)
                        G.add_edge(v, x)

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


def inter_random_2k(G, node_community, n_swap=1, max_tries=100, connected=1):
    """Returns a 2K null model beased on random reconnection algorithm inter communities

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 2k-characteristic unchanged and the graph connected.
    Swap edges inter communities.

    """
    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated.
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inner community.
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:
                # Make sure the edges created are inner community.
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:
                    # Keep the degree matching characteristic of nodes
                    # unchanged.
                    if G.degree(v) == G.degree(y):
                        # Make sure the new edges are not exist in the original
                        # graph.
                        if (y not in G[u]) and (v not in G[x]):
                            G.add_edge(u, y)
                            G.add_edge(v, x)

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


def inter_random_25k(G, node_community, n_swap=1, max_tries=100, connected=1):
    """Returns a 2.5K null model beased on random reconnection algorithm inter communities

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 2.5k-characteristic unchanged and the graph connected.
    Swap edges inter communities.

    """
    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated.
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inner community.
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:
                # Make sure the edges created are inner community.
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:
                    # Keep the degree matching characteristic of nodes
                    # unchanged.
                    if G.degree(v) == G.degree(y):
                        # Make sure the new edges are not exist in the original
                        # graph.
                        if (y not in G[u]) and (v not in G[x]):
                            G.add_edge(u, y)
                            G.add_edge(v, x)

                            G.remove_edge(u, v)
                            G.remove_edge(x, y)

                            degree_node_list = map(lambda t: (t[1], t[0]), G.degree(
                                [u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])).items())

                            D = count_degree_nodes(degree_node_list)
                            for i in range(len(D)):
                                avcG = nx.average_clustering(
                                    G, nodes=D.values()[i], weight=None, count_zeros=True)
                                avcG = nx.average_clustering(
                                    G, nodes=D.values()[i], weight=None, count_zeros=True)
                                i += 1
                                # If the degree-related clustering coefficient changed after scrambling
                                # withdraw this operation about scrambling.
                                if avcG != avcG:
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    break
                                # if connected = 1 but the original graph is not connected fully,
                                # withdraw the operation about the swap of
                                # edges.
                                if connected == 1:
                                    if not nx.is_connected(G):
                                        G.add_edge(u, v)
                                        G.add_edge(x, y)
                                        G.remove_edge(u, y)
                                        G.remove_edge(x, v)
                                        continue
                                swapcount += 1

    return G


def inter_random_3k(G, node_community, n_swap=1, max_tries=100, connected=1):
    """Returns a 3K null model beased on random reconnection algorithm inter communities

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 3k-characteristic unchanged and the graph connected.
    Swap edges inter communities.

    """
    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated.
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inter communities.
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:
                # Make sure the edges created are inner community.
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:
                    # Keep the degree matching characteristic of nodes
                    # unchanged.
                    if G.degree(v) == G.degree(y):

                        # Make sure the new edges are not exist in the original
                        # graph.
                        if (y not in G[u]) and (v not in G[x]):
                            G.add_edge(u, y)
                            G.add_edge(v, x)

                            G.remove_edge(u, v)
                            G.remove_edge(x, y)

                            # Get the set of four nodes and their neighbor
                            # nodes.
                            node_list = [
                                u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])
                            # Calculate the clustering coefficient of all these
                            # nodes in the original graph and the new graph.
                            avcG = nx.clustering(G, nodes=node_list)
                            avcG = nx.clustering(G, nodes=node_list)
                            # Keep the clustering coefficient of four nodes equal.
                            # Withdraw the operation about the swap of edges,
                            # otherwise.
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


def inner_community_swap(G, node_community, n_swap=1, max_tries=100):
    """

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Keep the degree distribution unchanged.
    Swap edges inner communities.

    """
    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated.
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges created are inner community.
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:
                # Make sure the edges created are inner community.
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:
                    # Make sure the new edges are not exist in the original
                    # graph.
                    if (y not in G[u]) and (v not in G[x]):
                        G.add_edge(u, y)
                        G.add_edge(v, x)

                        G.remove_edge(u, v)
                        G.remove_edge(x, y)

                        swapcount += 1
    return G


def inter_community_swap(G, node_community, n_swap=1, max_tries=100):
    """

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Keep the degree distribution unchanged.
    Swap edges inter communities.

    """
    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated.
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inter communities.
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:
                # Make sure the edges created are inter communities.
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:
                    # Make sure the new edges are not exist in the original
                    # graph.
                    if (y not in G[u]) and (v not in G[x]):
                        G.add_edge(u, y)
                        G.add_edge(v, x)

                        G.remove_edge(u, v)
                        G.remove_edge(x, y)

                        swapcount += 1

    return G


def Q_enhense(G, node_community, n_swap=1, max_tries=100):
    """

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Keep the degree distribution unchanged.
    Enhance the characteristics of the community structure

    """

    judge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated.
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inter communities.
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:
                # Make sure the edges created are inner community.
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:
                    # Make sure the new edges are not exist in the original
                    # graph.
                    if (y not in G[u]) and (v not in G[x]):
                        G.add_edge(u, y)
                        G.add_edge(v, x)

                        G.remove_edge(u, v)
                        G.remove_edge(x, y)

                        swapcount += 1

    return G


def Q_weaken(G, node_community, n_swap=1, max_tries=100):
    """

    Parameters
    ----------
    G : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Keep the degree distribution unchanged.
    Weaken the characteristics of the community structure

    """

    udge_error(G, n_swap, max_tries, connected)

    # Number of attempts to swap
    n_try = 0
    # Number of effective swaps
    swapcount = 0

    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s)' % swapcount)
            break
        n_try += 1

        # Keep the degree distribution unchanged,choose two edges (u-v,x-y)
        # randomly
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        # Make sure the four nodes are not repeated.
        if len(set([u, v, x, y])) == 4:
            # Make sure the chosen edges are inner community.
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:
                # Make sure the edges created are inter communities.
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:
                    # Make sure the new edges are not exist in the original
                    # graph.
                    if (y not in G[u]) and (v not in G[x]):
                        G.add_edge(u, y)
                        G.add_edge(v, x)

                        G.remove_edge(u, v)
                        G.remove_edge(x, y)

                        swapcount += 1

    return G
