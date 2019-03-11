# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 11:58:17 2015

@author: xiaokeeie
"""

import networkx as nx
import unweight_null_model as nm
import matplotlib.pyplot as plt


#G0=nx.barabasi_albert_graph(100, 4, seed=None)
#
#fh=open("BA_origin.txt",'wb')
#nx.write_edgelist(G0, fh, data=False)
#fh.close()
#n=len(G0.nodes())
#m=len(G0.edges())
#print n
#print m
#

fh=open("hot.txt", 'rb')
G=nx.read_edgelist(fh)
fh.close()
G0 = G.to_undirected()


nswap=500
max_tries=2000
rich_degree=4

#
#G1=nm.ER_model(G0) 
#fh=open("BA_er.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1


#G1=nm.config_model(G0) 
#fh=open("BA_config.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#G1 = nm.random_0kc(G0,nswap,max_tries)
#fh=open("BA_0kc.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#G1 = nm.random_1k(G0, nswap, max_tries)
#fh=open("BA_1k.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#
#G1 = nm.random_1kc(G0, nswap=100)
#fh=open("BA_1kc.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#
#G1 = nm.random_2k(G0,nswap,max_tries)
#fh=open("BA_2k.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#G1 = nm.random_2kc(G0,nswap,max_tries)
#fh=open("BA_2kc.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#G1 = nm.random_25k(G0,nswap,max_tries)
#fh=open("BA_25k.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#avcG0 = nx.average_clustering(G0)
#avcG = nx.average_clustering(G1)
#print n1
#print m1
#print avcG0,avcG
#
#G1 = nm.random_25kc(G0,nswap,max_tries)
#fh=open("BA_25kc.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#avcG0 = nx.average_clustering(G0)
#avcG = nx.average_clustering(G1)
#print n1
#print m1
#print avcG0,avcG
#
#
#
#G1 = nm.rich_club_creat(G0, rich_degree, max_tries)
#fh=open("BA_rich.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#
#G1 = nm.rich_club_creatc(G0, rich_degree, max_tries)
#fh=open("BA_richc.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1

G1 = nm.rich_club_break(G0, rich_degree, nswap, max_tries, connected=0)
fh=open("hot_norich.txt",'wb')
nx.write_edgelist(G1, fh, data=False)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1

nx.draw(G1)

#G1 = nm.rich_club_breakc(G0, rich_degree)
#fh=open("BA_norichc.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#G1 = nm.assort_mixing(G0,nswap,max_tries)
#fh=open("BA_assort.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#G1 = nm.assort_mixingc(G0,nswap,max_tries)
#fh=open("BA_assortc.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#G1 = nm.disassort_mixing(G0,nswap,max_tries)
#fh=open("BA_disassort.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#G1 = nm.disassort_mixingc(G0,nswap,max_tries)
#fh=open("BA_disassortc.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
#
#fh=open("BA_origin.txt", 'rb')
#H=nx.read_edgelist(fh,create_using=nx.DiGraph())
#fh.close()
#n=len(H.nodes())
#m=len(H.edges())
#print n
#print m
#
#
#G1 = nm.random_1kd(H,nswap,max_tries)
#fh=open("BA_1kd.txt",'wb')
#nx.write_edgelist(G1, fh, data=False)
#fh.close()
#n1=len(G1.nodes())
#m1=len(G1.edges())
#print n1
#print m1
