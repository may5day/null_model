import networkx as nx
import random
import copy
"""
+ : weight=1
- : weight=2
"""

def sign_network_positive_swap(G0, nswap=1, max_tries=100):    

    G=copy.deepcopy(G0)
    n=0
    swapcount=0
    keys,degrees=zip(*G.degree().items())           # keys, degree
    cdf=nx.utils.cumulative_distribution(degrees)   # cdf of degree
    
    while swapcount < nswap:
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue # same source, skip
        u=keys[ui] # convert index to label
        x=keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u]))>0 and len(list(G[x]))>0:
            v=random.choice(list(G[u]))
            y=random.choice(list(G[x]))
            if v==y:
                continue
        else:
            continue
        
        if (x not in G[u]) and (y not in G[v]) and G[u][v]['weight']==1 and G[x][y]['weight']==1:
                        if connected==1:                            #判断是否需要保持联通特性，为1的话则需要保持该特性        
                    if not nx.is_connected(G):              #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                    	G.add_edge(u,v)
                    	G.add_edge(x,y)
                    	G.remove_edge(u,y)
                    	G.remove_edge(x,v)
                    	continue 
                swapcount=swapcount+1    
            G.add_edge(u,x,weight=1)
            G.add_edge(v,y,weight=1)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            swapcount+=1
            
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n + 'before desired swaps achieved (%s).'%nswap)
            print nx.NetworkXAlgorithmError(e)
            break
        n+=1
        if n%1000000==0:
            print 'swap times=',swapcount,'try times=',n
    return G
    
def sign_network_negative_swap(G0, nswap=1, max_tries=100):    
    # Instead of choosing uniformly at random from a generated edge list,
    # this algorithm chooses nonuniformly from the set of nodes with
    # probability weighted by degree.
    G=copy.deepcopy(G0)
    n=0
    swapcount=0
    keys,degrees=zip(*G.degree().items()) # keys, degree
    cdf=nx.utils.cumulative_distribution(degrees)  # cdf of degree
        
    
    while swapcount < nswap:
#        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue # same source, skip
        u=keys[ui] # convert index to label
        x=keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u]))>0 and len(list(G[x]))>0:
            v=random.choice(list(G[u]))
            y=random.choice(list(G[x]))
            if v==y:
                continue
        else:
            continue
        
        if (x not in G[u]) and (y not in G[v]) and G[u][v]['weight']==2 and G[x][y]['weight']==2:
            G.add_edge(u,x,weight=2)
            G.add_edge(v,y,weight=2)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            swapcount+=1
            
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n + 'before desired swaps achieved (%s).'%nswap)
            print nx.NetworkXAlgorithmError(e)
            break
        n+=1
        if n%1000000==0:
            print 'swap times=',swapcount,'try times=',n
    return G
    
def sign_network_sign_swap(G0, nswap=1, max_tries=100):    
    # Instead of choosing uniformly at random from a generated edge list,
    # this algorithm chooses nonuniformly from the set of nodes with
    # probability weighted by degree.
    G=copy.deepcopy(G0)
    n=0
    swapcount=0
    keys,degrees=zip(*G.degree().items()) # keys, degree
    cdf=nx.utils.cumulative_distribution(degrees)  # cdf of degree        
    
    while swapcount < nswap:
#        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue # same source, skip
        u=keys[ui] # convert index to label
        x=keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u]))>0 and len(list(G[x]))>0:
            v=random.choice(list(G[u]))
            y=random.choice(list(G[x]))
            if v==y:
                continue
            G[u][v]['weight'],G[x][y]['weight'] = G[x][y]['weight'],G[u][v]['weight']
            if G[u][v]['weight']!=G[x][y]['weight']:
                swapcount+=1
                
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n + 'before desired swaps achieved (%s).'%nswap)
            print nx.NetworkXAlgorithmError(e)
            break
        n+=1
        if n%1000000==0:
            print 'swap times=',swapcount,'try times=',n
    return G
    
def sign_network_full_swap(G0, nswap=1, max_tries=100):    
    # Instead of choosing uniformly at random from a generated edge list,
    # this algorithm chooses nonuniformly from the set of nodes with
    # probability weighted by degree.
    G=copy.deepcopy(G0)
    n=0
    swapcount=0
    keys,degrees=zip(*G.degree().items()) # keys, degree
    cdf=nx.utils.cumulative_distribution(degrees)  # cdf of degree
        
    
    while swapcount < nswap:
#        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue # same source, skip
        u=keys[ui] # convert index to label
        x=keys[xi]
        # choose target uniformly from neighbors
        if len(list(G[u]))>0 and len(list(G[x]))>0:
            v=random.choice(list(G[u]))
            y=random.choice(list(G[x]))
            if v==y:
                continue
            if (x not in G[u]) and (y not in G[v]):
                G.add_edge(u,x,weight=G[u][v]['weight'])
                G.add_edge(v,y,weight=G[x][y]['weight'])
                G.remove_edge(u,v)
                G.remove_edge(x,y)
                swapcount+=1
            
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n + 'before desired swaps achieved (%s).'%nswap)
            print nx.NetworkXAlgorithmError(e)
            break
        n+=1
        if n%1000000==0:
            print 'swap times=',swapcount,'try times=',n
    return G
