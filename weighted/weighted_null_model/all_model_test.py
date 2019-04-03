# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 11:58:17 2015

@author: xiaokeeie
"""

import pickle
import networkx as nx
import weighted_nullmodel as wnm
import numpy as np

'''
data = pickle.load(open('sms_network.pk', 'rb'))
data1 = [tuple(e) for e in data]
G=nx.Graph()
G.add_weighted_edges_from(data1)
num_comp = nx.number_connected_components(G)#26544
list_G = list(nx.connected_component_subgraphs(G))#原始网络的连通子图
#==============================================================================
# 子图的规模
#l = []
#for i in range(len(list_G)):
#    e = list_G[i]
#    l.append(len(e.nodes()))
#    if len(e.nodes())>55 and len(e.nodes())<70:
#        print i
#print set(l)
# [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 
# 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 36, 
# 37, 46, 51, 67, 70992]
# 70992-> list_G[0]
#==============================================================================


#==============================================================================
# 需要和老师验证一下：
# 老师所给的图有148249条边，142219个节点，连通子图26544，其中规模最大规模连通子图含70992个节点，其余子图规模较小
# 1. 保持连通性置乱，需要原始网络必须是连通图吗？
# 目前程序是按输入网络必须是连通图才可以执行保持连通性置乱（我认为这样是正确的）。
# 记得老师曾经说保持连通置乱是对连通子图进行置乱，所以可以理解为，
# 不要求输入网络必须是连通图，只要其连通子图置乱后仍保持连通性就可以，对吗？
# 问题：那我对一个有多个连通子图的非连通图进行保持连通性置乱，在调用置乱算法前先取得原始网络的连通子图，
# 然后依次传入子图进行保持联通性置乱，可以吗？还是需要修改保持连通性置乱算法的程序？
# 2.目前验证程序是否正确，我先取一个规模适中的连通子图可以不？ 比如说含有67个节点的连通子图（规模次大），还是要怎么取样本？
  
#==============================================================================
#==============================================================================
# fh=open("origin0.txt",'wb')
# nx.write_weighted_edgelist(G, fh)
# fh.close()
#==============================================================================

G0 = list_G[3763]
if nx.is_connected(G0):
    print 'True'
    
fh=open("origin.txt",'wb')
nx.write_weighted_edgelist(G0, fh)
fh.close()
n=len(G0.nodes())
m=len(G0.edges())
print n
print m

'''

fh=open("origin.txt", 'rb')
G=nx.read_weighted_edgelist(fh)
fh.close()
G0 = G.to_undirected()
n=len(G0.nodes())
m=len(G0.edges())
print n
print m



nswap=200
max_tries=1000
rich_degree=3

#0k 与原始网络具有相同的节点数和平均度
G1 = wnm.random_0k(G0,nswap,max_tries)
fh=open("wnm_0k.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print 'random_0k:节点数和平均度'
if n1 == n and m1 == m:
    print "与原始网络有相同的节点数"
if np.mean(G0.degree().values()) == np.mean(G1.degree().values()):
    print "与原始网络有相同的平均度"



#==============================================================================
G1 = wnm.random_0kc(G0,nswap,max_tries)
fh=open("wnm_0kc.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n
print m
#==============================================================================


#1K 具有相同的节点度分布
G1 = wnm.random_1k(G0, nswap, max_tries)
#G1 = nx.double_edge_swap(G0, nswap, max_tries)
fh=open("wnm_1k.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print 'random_1k:节点数和节点度分布'
if n1 == n and m1 == m:
    print "与原始网络有相同的节点数"
if G0.degree() == G1.degree():
    print "与原始网络有相同的节点度分布"


#==============================================================================
G1 = wnm.random_1kc(G0, nswap, max_tries)
fh=open("wnm_1kc.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1
#==============================================================================


#等权重置乱
G1 = wnm.random_sw(G0,nswap,max_tries)
fh=open("wnm_sw.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print 'random_sw:节点数和节点度分布'
if n1 == n and m1 == m:
    print "与原始网络有相同的节点数"
if G0.degree() == G1.degree():
    print "与原始网络有相同的节点度分布"

#==============================================================================
G1 = wnm.random_swc(G0,nswap,max_tries)
fh=open("wnm_swc.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1
#==============================================================================

#权重置乱
G1 = wnm.random_w(G0,nswap,max_tries)
fh=open("wnm_w.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print 'random_w:节点数和节点度分布'
if n1 == n and m1 == m:
    print "与原始网络有相同的节点数"
if G0.degree() == G1.degree():
    print "与原始网络有相同的节点度分布"


G1 = wnm.rich_club_creat(G0, rich_degree, max_tries)
fh=open("wnm_rich.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print 'rich_club_creat:'
if n1 == n and m1 == m:
    print "与原始网络有相同的节点数"
if G0.degree() == G1.degree():
    print "与原始网络有相同的节点度分布"

#==============================================================================
# UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 63: ordinal not in range(128)
#==============================================================================
#==============================================================================
G1 = wnm.rich_club_creatc(G0, rich_degree, max_tries)
fh=open("wnm_richc.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1
#==============================================================================

G1 = wnm.rich_club_break(G0, rich_degree, max_tries)
fh=open("wnm_norich.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1

#==============================================================================
G1 = wnm.rich_club_breakc(G0, rich_degree, max_tries)
fh=open("wnm_norichc.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1
#==============================================================================

G1 = wnm.assort_mixing(G0,nswap,max_tries)
fh=open("wnm_assort.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1

#==============================================================================
G1 = wnm.assort_mixingc(G0,nswap,max_tries)
fh=open("wnm_assortc.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1
#==============================================================================

G1 = wnm.disassort_mixing(G0,nswap,max_tries)
fh=open("wnm_disassort.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1


#==============================================================================
G1 = wnm.disassort_mixingc(G0,nswap,max_tries)
fh=open("wnm_disassortc.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1
#==============================================================================

fh=open("origin.txt", 'rb')
H=nx.read_weighted_edgelist(fh,create_using=nx.DiGraph())
fh.close()
n=len(H.nodes())
m=len(H.edges())
print n
print m


G1 = wnm.random_1kd(H,nswap,max_tries)
fh=open("wnm_1kd.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1

#==============================================================================
G1 = wnm.random_1kcd(H,nswap,max_tries)
fh=open("wnm_1kcd.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1
##==============================================================================

G1 = wnm.random_out_lw(H,nswap,max_tries)
fh=open("wnm_1kd_out.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1

G1 = wnm.random_in_lw(H,nswap,max_tries)
fh=open("wnm_1kd_in.txt",'wb')
nx.write_weighted_edgelist(G1, fh)
fh.close()
n1=len(G1.nodes())
m1=len(G1.edges())
print n1
print m1

