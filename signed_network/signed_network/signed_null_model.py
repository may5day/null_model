import networkx as nx
import random
import copy
"""
+ : weight=1
- : weight=2
"""
__all__ = ['snd_pos_swap',
           'snd_neg_swap',
           'snd_sign_swap',
           'snd_full_swap',
           'snd_swap',
           'sn_pos_swap',
           'sn_neg_swap',
           'sn_sign_swap',
           'sn_full_swap']


def snd_pos_swap(G, n_swap=1, max_tries=100):
    """Returns a 1K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : directed graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Instead of choosing uniformly at random from a generated edge list,
    this algorithm chooses nonuniformly from the set of nodes with probability weighted by degree.
    The out degree of each node remains unchanged after swap.

    See Also
    --------
    sn_pos_swap

    """
    n_try = 0
    swapcount = 0
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)  # cdf of degree

    while swapcount < n_swap:
        #        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue

        if (x not in G[u]) and (y not in G[v]) and G[u][v]['weight'] == 1 and G[x][y]['weight'] == 1:

            if ((u in G[x]) and (G[x][u]['weight'] == 2)) or ((v in G[y]) and (G[y][v]['weight'] == 2)):
                continue
            else:
                G.add_edge(u, x, weight=1)
                G.add_edge(v, y, weight=1)
                G.remove_edge(u, v)
                G.remove_edge(x, y)
                swapcount += 1
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
        if n_try % 100000 == 0:
            print('swap times=', swapcount, 'try times=', n_try)
    return G


def snd_neg_swap(G, n_swap=1, max_tries=100):
    """Returns a 1K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : directed graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Instead of choosing uniformly at random from a generated edge list,
    this algorithm chooses nonuniformly from the set of nodes with probability weighted by degree.
    The in degree of each node remains unchanged after swap.

    See Also
    --------
    sn_neg_swap

    """

    n_try = 0
    swapcount = 0
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)  # cdf of degree

    while swapcount < n_swap:
        #        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue

        if (x not in G[u]) and (y not in G[v]) and G[u][v]['weight'] == 2 and G[x][y]['weight'] == 2:

            if ((u in G[x]) and (G[x][u]['weight'] == 1)) or ((v in G[y]) and (G[y][v]['weight'] == 1)):
                continue
            else:
                G.add_edge(u, x, weight=2)
                G.add_edge(v, y, weight=2)
                G.remove_edge(u, v)
                G.remove_edge(x, y)
                swapcount += 1
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
        if n_try % 100000 == 0:
            print('swap times=', swapcount, 'try times=', n_try)
    return G


def snd_sign_swap(G, n_swap=1, max_tries=100):
    """Returns a 1K null model

    Parameters
    ----------
    G : directed graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Instead of choosing uniformly at random from a generated edge list,
    this algorithm chooses nonuniformly from the set of nodes with probability weighted by degree.
    The topological structure of this network remains unchanged after scrambling.

    See Also
    --------
    sn_sign_swap

    """

    n_try = 0
    swapcount = 0
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)  # cdf of degree

    while swapcount < n_swap:
        #        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue

        if (G.is_directed() and u in G[v]) or (G.is_directed() and x in G[y]):
            continue
        else:
            G[u][v]['weight'], G[x][y]['weight'] = G[
                x][y]['weight'], G[u][v]['weight']
            if G[u][v]['weight'] != G[x][y]['weight']:
                swapcount += 1
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
        if n_try % 100000 == 0:
            print('swap times=', swapcount, 'try times=', n_try)
    return G


def snd_full_swap(G, n_swap=1, max_tries=100):
    """Returns a 1K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : directed graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Instead of choosing uniformly at random from a generated edge list,
    this algorithm chooses nonuniformly from the set of nodes with probability weighted by degree.
    The degree of each node and topological structure of this network changed after swap.

    See Also
    --------
    sn_full_swap

    """

    n = 0
    swapcount = 0
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)  # cdf of degree

    while swapcount < n_swap:
        #        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue

        if (x not in G[u]) and (y not in G[v]):

            if (u in G[x]) or (v in G[y]):
                continue
            else:
                G.add_edge(u, x, weight=G[u][v]['weight'])
                G.add_edge(v, y, weight=G[x][y]['weight'])
                G.remove_edge(u, v)
                G.remove_edge(x, y)
                swapcount += 1
        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
        if n_try % 100000 == 0:
            print('swap times=', swapcount, 'try times=', n_try)
    return G


def snd_swap(G, n_swap=1, max_tries=100, paradox='false'):
    """Returns a 1K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : directed graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Instead of choosing uniformly at random from a generated edge list,
    this algorithm chooses nonuniformly from the set of nodes with probability weighted by degree.
    The degree of each node remains unchanged after swap.

    """

    n_try = 0
    swapcount = 0
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)  # cdf of degree

    while swapcount < n_swap:
        #        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue

        if (paradox.lower() == 'true' and (u in G[v])) or (paradox.lower() == 'true' and (x in G[y])):
            continue

        else:
            G[u][v]['weight'], G[x][y]['weight'] = G[
                x][y]['weight'], G[u][v]['weight']
            if G[u][v]['weight'] != G[x][y]['weight']:
                swapcount += 1

        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
        if n_try % 1000000 == 0:
            print('swap times=', swapcount, 'try times=', n_try)
    return G


def sn_pos_swap(G, n_swap=1, max_tries=100):
    """Returns a 1K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : undirected graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Instead of choosing uniformly at random from a generated edge list,
    this algorithm chooses nonuniformly from the set of nodes with probability weighted by degree.
    The degree of each node remains unchanged after swap.

    See Also
    --------
    snd_pos_swap

    """

    n_try = 0
    swapcount = 0
    keys, degrees = zip(*G.degree().items())         
    cdf = nx.utils.cumulative_distribution(degrees)   # cdf of degree

    while swapcount < n_swap:
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue

        if (x not in G[u]) and (y not in G[v]) and G[u][v]['weight'] == 1 and G[x][y]['weight'] == 1:
            if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                if not nx.is_connected(G):  # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                    G.add_edge(u, v)
                    G.add_edge(x, y)
                    G.remove_edge(u, y)
                    G.remove_edge(x, v)
                    continue
                swapcount = swapcount + 1
            G.add_edge(u, x, weight=1)
            G.add_edge(v, y, weight=1)
            G.remove_edge(u, v)
            G.remove_edge(x, y)
            swapcount += 1

        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
        if n_try % 1000000 == 0:
            print('swap times=', swapcount, 'try times=', n_try)
    return G


def sn_neg_swap(G, n_swap=1, max_tries=100):
    """Returns a 1K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : directed graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Instead of choosing uniformly at random from a generated edge list,
    this algorithm chooses nonuniformly from the set of nodes with probability weighted by degree.
    The degree of each node remains unchanged after swap.

    See Also
    --------
    snd_neg_swap

    """

    n_try = 0
    swapcount = 0
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)  # cdf of degree

    while swapcount < n_swap:
        #        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue

        if (x not in G[u]) and (y not in G[v]) and G[u][v]['weight'] == 2 and G[x][y]['weight'] == 2:
            G.add_edge(u, x, weight=2)
            G.add_edge(v, y, weight=2)
            G.remove_edge(u, v)
            G.remove_edge(x, y)
            swapcount += 1

        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
        if n_try % 1000000 == 0:
            print('swap times=', swapcount, 'try times=', n_try)
    return G


def sn_sign_swap(G, n_swap=1, max_tries=100):
    """Returns a 1K null model

    Parameters
    ----------
    G : directed graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Instead of choosing uniformly at random from a generated edge list,
    this algorithm chooses nonuniformly from the set of nodes with probability weighted by degree.
    The topological structure of this network remains unchanged after scrambling.

    See Also
    --------
    snd_sign_swap

    """

    n_try = 0
    swapcount = 0
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)  # cdf of degree

    while swapcount < n_swap:
        #        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
            G[u][v]['weight'], G[x][y]['weight'] = G[
                x][y]['weight'], G[u][v]['weight']
            if G[u][v]['weight'] != G[x][y]['weight']:
                swapcount += 1

        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
        if n_try % 1000000 == 0:
            print('swap times=', swapcount, 'try times=', n_try)
    return G


def sn_full_swap(G, n_swap=1, max_tries=100):
    """Returns a 1K null model beased on random reconnection algorithm

    Parameters
    ----------
    G : directed graph
    n_swap : int (default = 1)
        Number of double-edge swaps to perform
    max_tries : int (default = 100)
        Maximum number of attempts to swap edges

    Notes
    -----
    Instead of choosing uniformly at random from a generated edge list,
    this algorithm chooses nonuniformly from the set of nodes with probability weighted by degree.
    The degree of each node and topological structure of this network changed after swap.

    See Also
    --------
    snd_full_swap

    """

    n_try = 0
    swapcount = 0
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)  # cdf of degree

    while swapcount < n_swap:
        #        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
            if (x not in G[u]) and (y not in G[v]):
                G.add_edge(u, x, weight=G[u][v]['weight'])
                G.add_edge(v, y, weight=G[x][y]['weight'])
                G.remove_edge(u, v)
                G.remove_edge(x, y)
                swapcount += 1

        if n_try >= max_tries:
            print('Maximum number of swap attempts (%s) exceeded ' %
                  n_try + 'before desired swaps achieved (%s).' % n_swap)
            break
        n_try += 1
        if n_try % 1000000 == 0:
            print('swap times=', swapcount, 'try times=', n_try)
    return G