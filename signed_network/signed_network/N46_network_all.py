#-*- coding:utf-8 -*-
import networkx as nx
import signedmodel as sm


filename = 'N46edge.txt'
##filename = 'epinions_test.txt'
#
def loadfile():
    with open(filename) as f:
        edges = []
        for each_line in f:
            #print each_line
            n1,n2,w = each_line.strip('\t\r\n').split('\t')
            edges.append((n1,n2,int(w)))
        return edges
        
nswap=2000
max_tries=5000
swap_time=1

G = nx.Graph()
G.add_weighted_edges_from(loadfile())
        

for i in range(1,swap_time+1):
    print 'positive_edges_swap_times_'+str(i)
    G1 = sm.sign_network_positive_swap(G, nswap, max_tries)
    filename1 = 'N46edge_positive_swap_nd_'+str(i)+'.txt'
    with open(filename1,'w')as f1:
        nx.write_weighted_edgelist(G1, f1)


for i in range(1,swap_time+1):
    print 'negative_edges_swap_times_d'+str(i)        
    G1 = sm.sign_network_negative_swap(G, nswap, max_tries)
    filename1 = 'N46edge_negative_swap_nd_'+str(i)+'.txt'
    with open(filename1,'w')as f1:
        nx.write_weighted_edgelist(G1, f1)
        
for i in range(1,swap_time+1):
    print 'negative_edges_swap_times_d'+str(i)        
    G1 = sm.sign_network_negative_swap(G, nswap, max_tries)
    G2 = sm.sign_network_positive_swap(G1, nswap, max_tries)
    filename1 = 'N46edge_pn_swap_nd_'+str(i)+'.txt'
    with open(filename1,'w')as f1:
        nx.write_weighted_edgelist(G2, f1)

for i in range(1,swap_time+1): 
    print 'sign_edges_swap_times_'+str(i)       
    G1 = sm.sign_network_sign_swap(G, nswap, max_tries)
    filename1 = 'N46edge_sign_swap_nd_'+str(i)+'.txt'
    with open(filename1,'w')as f1:
        nx.write_weighted_edgelist(G1, f1)  

for i in range(1,swap_time+1):      
    print 'fully_swap_times_'+str(i)
    G1 = sm.sign_network_full_swap(G, nswap, max_tries)
    filename1 = 'N46edge_full_swap_nd_'+str(i)+'.txt'
    with open(filename1,'w')as f1:
        nx.write_weighted_edgelist(G1, f1)  
