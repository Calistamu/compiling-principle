'''

用graphviz实现可视化
'''
from graphviz import Digraph

from NFAtoDFA import *
from DFAtoMDFA import *
from firstwork_retoNFA import * 


def graph_Nfa(ls,end):
    g = Digraph('NFA')
    for i in ls:
        for j in i:
            g.node(name = str(j))
            for k in i[j]:
                if i[j][k] == end:
                    g.node(name = str(i[j][k]),shape = 'doublecircle')
                else:
                    g.node(name = str(i[j][k]))       
                g.edge(str(j),str(i[j][k]),str(k))
    g.view()
def graph_Dfa(ls,ls1):
    g = Digraph('DFA')
    for i in ls:
        for j in i:
            if j in ls1:
                g.node(name = str(j),shape = 'doublecircle')
            else:
                g.node(name = str(j))
            for k in i[j]:
                if i[j][k] in ls1:
                    g.node(name = str(i[j][k]),shape = 'doublecircle')
                else:
                    g.node(name = str(i[j][k]))
                g.edge(str(j),str(i[j][k]),str(k))
    g.view()
def graph_MDfa(dic,ls1,ls):
    g = Digraph('MDFA')
    for i in dic:
        if i in ls1:
            g.node(name = str(i))
        for j in range(len(dic[i])):
            t = dic[i][j][0]
            if t != -1:
                if t in ls1:
                    g.node(name = str(t),shape = 'doublecircle')
                else:
                    g.node(name = str(t))
                g.edge(str(i),str(t),str(ls[j]))
    g.view()
