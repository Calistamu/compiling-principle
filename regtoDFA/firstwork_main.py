'''
从正则表达式（中缀表达式）到逆波兰表达式到NFA到DFA到最小化DFA最后实现可视化
'''
from firstwork_re import *
from firstwork_retoNFA import *
from ClosureAndMove import *
from NFAtoDFA import *
from DFAtoMDFA import *
from Graphsum import *

if __name__ == '__main__':
#     str1 = add_sign("a(b|c)*")
#     str1 = add_sign("(ab)*(a*|b*)(ba)*")
    str1 = add_sign("ab|c(d*|a)")
    print("加入乘法点的表达式：{0}".format(str1))
#     ls = shunting_yard("(a|b)*abb")
#     ls = shunting_yard("(ab)*(a*|b*)(ba)*")
#     ls = shunting_yard("a(b|c)*")
    ls = shunting_yard("aa*bb*")
    print("转成逆波兰表达式：{0}".format(ls))
    start,end,ls1 = retoNFA(ls)
    print(end)
    print("转成nfa：{0}".format(ls1))
    graph_Nfa(ls1,end)
    N = Nfa(start,end,ls1)
    D = Dfa(N,ls)
    a = D.move
    print("状态集合标号数组:{0}".format(D.dt))
    print("dfa转移表：{0}".format(D.move))
    print("终态为：{0}".format(D.ls_accepted))
    print("除终态外的另一个状态：{0}".format(D.ls_notaccepted))
    graph_Dfa(a,D.ls_accepted)
    MD = toMiniDfa(D.ls_notaccepted,D.ls_accepted,D.ls1,D.move,D.dic1,D.dt)
    
    print("最小化后DFA的终态为：{0}".format(MD.accepted1))
    print("最小化后dfa的非终态为：{0}".format(MD.notaccepted1))
    print("最小化后dfa的分组为：{0}".format(MD.dic_region))
    print("最小化后dfa的分组标准为：{0}".format(MD.dic_regionstandard))
    graph_MDfa(MD.dic_regionstandard,MD.accepted1 ,D.ls1)
#     print(start,end,ls1)

    