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
           'Q_increase',
           'Q_decrease', ]


def judge_error(G0, n_swap, max_tries, connected):
    if not nx.is_connected(G0):
        raise nx.NetworkXError("For connected graphs only.")
    if G0.is_directed():
        raise nx.NetworkXError("For undirected graphs only.")
    if n_swap > max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
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


def inner_random_1k(G0, node_community, n_swap=1, max_tries=100, connected=1):
    """Returns a 1K null model beased on random reconnection algorithm

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the degree distribution unchanged and the graph connected.
    Swap edges inner communities.

    """
    judge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:

                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                    if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                        # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                        if not nx.is_connected(G):
                            G.add_edge(u, v)
                            G.add_edge(x, y)
                            G.remove_edge(u, y)
                            G.remove_edge(x, v)
                            continue
                    swapcount = swapcount + 1
    return G


def inner_random_2k(G0, node_community, n_swap=1, max_tries=100, connected=1):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 2k-characteristic unchanged and the graph connected.
    Swap edges inner communities.

    """
    judge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:

                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                if not nx.is_connected(G):
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    continue
                            swapcount = swapcount + 1
    return G


def inner_random_25k(G0, node_community, n_swap=1, max_tries=100, connected=1):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 2.5k-characteristic unchanged and the graph connected.
    Swap edges inner communities.

    """
    judge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:

                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            degree_node_list = map(lambda t: (t[1], t[0]), G0.degree(
                                [u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])).items())
                            # 先找到四个节点以及他们邻居节点的集合，然后取出这些节点所有的度值对应的节点，格式为（度，节点）形式的列表

                            # 找到每个度对应的所有节点，具体形式为
                            D = count_degree_nodes(degree_node_list)
                            for i in range(len(D)):
                                avcG0 = nx.average_clustering(
                                    G0, nodes=D.values()[i], weight=None, count_zeros=True)
                                avcG = nx.average_clustering(
                                    G, nodes=D.values()[i], weight=None, count_zeros=True)
                                i += 1
                                if avcG0 != avcG:  # 若置乱前后度相关的聚类系数不同，则撤销此次置乱操作
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    break
                                if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                    # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                    if not nx.is_connected(G):
                                        G.add_edge(u, v)
                                        G.add_edge(x, y)
                                        G.remove_edge(u, y)
                                        G.remove_edge(x, v)
                                        continue
                                swapcount = swapcount + 1

    return G


def inner_random_3k(G0, node_community, n_swap=1, max_tries=100, connected=1):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 3k-characteristic unchanged and the graph connected.
    Swap edges inner communities.

    """
    judge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:  # 保证所取的连边为社团间连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:
                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变

                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            # 找到四个节点以及他们邻居节点的集合
                            node_list = [
                                u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])
                            # 计算旧网络中4个节点以及他们邻居节点的聚类系数
                            avcG0 = nx.clustering(G0, nodes=node_list)
                            # 计算新网络中4个节点以及他们邻居节点的聚类系数
                            avcG = nx.clustering(G, nodes=node_list)

                            if avcG0 != avcG:  # 保证涉及到的四个节点聚类系数相同:若聚类系数不同，则撤回交换边的操作
                                G.add_edge(u, v)
                                G.add_edge(x, y)
                                G.remove_edge(u, y)
                                G.remove_edge(x, v)
                                continue
                            if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                if not nx.is_connected(G):
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    continue
                            swapcount = swapcount + 1
    return G


def inter_random_1k(G0, node_community, n_swap=1, max_tries=100, connected=1):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the degree distribution unchanged and the graph connected.
    Swap edges inter communities.

    """
    judge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:

                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                    if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                        # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                        if not nx.is_connected(G):
                            G.add_edge(u, v)
                            G.add_edge(x, y)
                            G.remove_edge(u, y)
                            G.remove_edge(x, v)
                            continue
                    swapcount = swapcount + 1
    return G


def inter_random_2k(G0, node_community, n_swap=1, max_tries=100, connected=1):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 2k-characteristic unchanged and the graph connected.
    Swap edges inter communities.

    """
    judge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:

                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                if not nx.is_connected(G):
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    continue
                            swapcount = swapcount + 1
    return G


def inter_random_25k(G0, node_community, n_swap=1, max_tries=100, connected=1):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 2.5k-characteristic unchanged and the graph connected.
    Swap edges inter communities.

    """
    judge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:

                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            degree_node_list = map(lambda t: (t[1], t[0]), G0.degree(
                                [u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])).items())
                            # 先找到四个节点以及他们邻居节点的集合，然后取出这些节点所有的度值对应的节点，格式为（度，节点）形式的列表

                            # 找到每个度对应的所有节点，具体形式为
                            D = count_degree_nodes(degree_node_list)
                            for i in range(len(D)):
                                avcG0 = nx.average_clustering(
                                    G0, nodes=D.values()[i], weight=None, count_zeros=True)
                                avcG = nx.average_clustering(
                                    G, nodes=D.values()[i], weight=None, count_zeros=True)
                                i += 1
                                if avcG0 != avcG:  # 若置乱前后度相关的聚类系数不同，则撤销此次置乱操作
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    break
                                if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                    # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                    if not nx.is_connected(G):
                                        G.add_edge(u, v)
                                        G.add_edge(x, y)
                                        G.remove_edge(u, y)
                                        G.remove_edge(x, v)
                                        continue
                                swapcount = swapcount + 1

    return G


def inter_random_3k(G0, node_community, n_swap=1, max_tries=100, connected=1):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes
    connected : int
        keep the connectivity of the graph or not.
        1 : keep,    0 : not keep

    Notes
    -----
    Keep the 3k-characteristic unchanged and the graph connected.
    Swap edges inter communities.

    """
    judge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:  # 保证所取的连边为社团间连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:
                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变

                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            # 找到四个节点以及他们邻居节点的集合
                            node_list = [
                                u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])
                            # 计算旧网络中4个节点以及他们邻居节点的聚类系数
                            avcG0 = nx.clustering(G0, nodes=node_list)
                            # 计算新网络中4个节点以及他们邻居节点的聚类系数
                            avcG = nx.clustering(G, nodes=node_list)

                            if avcG0 != avcG:  # 保证涉及到的四个节点聚类系数相同:若聚类系数不同，则撤回交换边的操作
                                G.add_edge(u, v)
                                G.add_edge(x, y)
                                G.remove_edge(u, y)
                                G.remove_edge(x, v)
                                continue
                            if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                if not nx.is_connected(G):
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    continue
                            swapcount = swapcount + 1
    return G


def inner_community_swap(G0, node_community, n_swap=1, max_tries=100):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes

    Notes
    -----
    Keep the degree distribution unchanged.
    Swap edges inner communities.

    """
    judge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:  # 保证所取的连边为社团内连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:
                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                        swapcount += 1  # 改变成功次数加1
    return G


def inter_community_swap(G0, node_community, n_swap=1, max_tries=100):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes

    Notes
    -----
    Keep the degree distribution unchanged.
    Swap edges inter communities.

    """
    judge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证为四个独立节点
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:  # 保证所取的连边是社团间部连边
                # 保证新生成的边是社团间的连边
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:
                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                        swapcount = swapcount + 1  # 改变成功次数加1

    return G


def Q_increase(G0, node_community, n_swap=1, max_tries=100):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes

    Notes
    -----
    Keep the degree distribution unchanged.
    Increase Q.

    """
    # 保证度分布不变的情况下，增强社团结构特性


    udge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community, (u, v)) == 0 and edge_in_community(node_community, (x, y)) == 0:  # 保证所取的连边为社团间连边
                # 保证新生成的边是内部连边
                if edge_in_community(node_community, (u, y)) == 1 and edge_in_community(node_community, (v, x)) == 1:
                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                        swapcount += 1  # 改变成功次数加1

    return G


def Q_decrease(G0, node_community, n_swap=1, max_tries=100):
    """

    Parameters
    ----------
    G0 : undirected and unweighted graph
    node_community : list
        nodes and the communities they belong to
    n_swap : int (default = 1)
        coefficient of change successfully
    max_tries : int (default = 100)
        number of changes

    Notes
    -----
    Keep the degree distribution unchanged.
    Decrease Q.

    """
    # 保证度分布不变的情况下，减弱社团结构特性


    udge_error(G0, n_swap, max_tries, connected)

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < n_swap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证为四个独立节点
            if edge_in_community(node_community, (u, v)) == 1 and edge_in_community(node_community, (x, y)) == 1:  # 保证所取的连边是社团内部连边
                # 保证新生成的边是社团间的连边
                if edge_in_community(node_community, (u, y)) == 0 and edge_in_community(node_community, (v, x)) == 0:
                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                        swapcount += 1  # 改变成功次数加1

    return G
