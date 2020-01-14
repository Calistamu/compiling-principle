'''
从NFA到DFA
'''
from ClosureAndMove import *
from firstwork_retoNFA import  *

class Dfa:
    def __init__(self,N,ls):
        self.Dfa_state_start = N.make_Closure([N.start])   #DFA的初态
        self.Dfa_statelist = [self.Dfa_state_start]        #存DFA的状态表
        self.Dfa_stateflag = {0:0}                         #记录DFA是否别标记过
        self.Dfa_state_accepted = N.accepted               #DFA的终态
        cnt = 0                                            #记录下标
        cnt_state = 0
        dt = {}                                             #方便检查
        ls_ans = []
        ls_accepted = []
        ls_notaccepted = []
        ls1 = N.get_alpha(ls) 
        if N.accepted in self.Dfa_state_start:#判断初始状态是在终结符状态里还是非终结符状态里
            ls_accepted = [0]
        else:
            ls_notaccepted = [0]        
        while cnt <= cnt_state and self.Dfa_stateflag[cnt] == 0:
            dt[cnt] = tuple(self.Dfa_statelist[cnt])
            for char in ls1:#遍历每个符号
                tup = tuple(N.make_Closure(N.make_move(self.Dfa_statelist[cnt],char)))#经过符号后产生的集合在做闭包运算
                for i in range(len(ls1)):
                    if char == ls1[i]:
                        dic = {}
                        dic1 = {}
                        dic1[char] = tup   #存放在字典里
                        dic[cnt] = dic1
                        ls_ans.append(dic)
                        break
                if tup not in self.Dfa_statelist and tup != () and self.is_numright(list(tup), self.Dfa_statelist)!=1:
                    self.Dfa_statelist.append(tup)
                    cnt_state += 1
                    self.Dfa_stateflag[cnt_state] = 0
                    if N.accepted in tup and cnt_state not in ls_accepted: #判断 终结符与非终结符
                        ls_accepted.append(cnt_state)
                    elif cnt_state not in ls_notaccepted:
                        ls_notaccepted.append(cnt_state)
            self.Dfa_stateflag[cnt] = 1
            cnt += 1
        self.dt = dt
        self.move = self.trans_second(ls_ans,dt)
        self.ls_accepted = ls_accepted
        self.ls_notaccepted = ls_notaccepted
        self.dic1 = dic1
        self.ls1 = ls1
    def trans(self,dt):
        dic1 = {}
        for i in dt.keys():
            tu = dt[i]
            dic1[tu] = i
        return dic1 
    def trans_second(self,ls,dt):
        ls1 = []
        for i in ls:
            for j in i:
                dic = i[j]
                for m in dic:
                    for n in dt:
                        if dt[n] == dic[m]:
                            dic[m] = n
        for i in ls:
            for j in i:
                dic = i[j]
                for m in dic:
                    if dic[m] != ():
                        ls1.append(i)
        return ls1
    def is_numright(self,list1,list2):
        for i in list2:
            if set(list1).issubset(set(i)) and set(i).issubset(set(list1)):
                flag = 1
                break
            else:
                flag = 0
        return  flag
            
                        
                         
        
        
