'''
用分割法最小化DFA
'''
from NFAtoDFA import *
import operator
            
class toMiniDfa:
    flag_mark = 1
    length = 0
    Region = []                        #记录分区
    dic_region = {} 
    standard = []
    dic_regionstandard = {}
    dic_regionstandard_accepted = {}
    dic_regionstandard_notaccepted = {}
    def __init__(self,ls_notaccepted,ls_accepted,ls,move,dic1,dic_goal):
        self.accepted = []
        self.notaccepted = []
        self.length = len(ls_notaccepted) + len(ls_accepted)
        self.Region.append(ls_notaccepted)
        self.Region.append(ls_accepted)
        self.accepted.append(ls_accepted)
        self.notaccepted.append(ls_notaccepted)
        self.dic_region[1] = ls_notaccepted
        self.dic_region[2] = ls_accepted
        self.flag_notaccepted = 1
        self.cnt = 2
        self.flag = 1
        while self.flag == 1:
            self.dic_regionstandard = {}
            self.dic_regionstandard_accepted = {}
            self.dic_regionstandard_notaccepted = {}
            self.flag = 0
            if self.flag_notaccepted == 1:
                for i in self.less_ls(self.Region,self.accepted):             #遍历每一个分区
                    dic_tempor = {}
                    for j in i:                   #遍历分区中的每一个状态
                        ls1 = []
                        for index in range(len(ls)):      #ls字母表
                            ls0 = []
                            ls0.append(self.get_goal(ls[index], move, j, dic1, self.dic_region))
                            ls1.append(ls0)
                        dic_tempor[j] = ls1
                        if j == i[0] :
                            for x in self.dic_region:
                                if i == self.dic_region[x]:
                                    self.dic_regionstandard[x] = ls1
                                    self.dic_regionstandard_notaccepted[x] = ls1
                    cnt = 0
                    while cnt<len(i):
                        if self.is_equal(dic_tempor[i[cnt]],dic_tempor[i[0]]) == 0:
                            self.flag = 1
                            t = self.is_inotherregion(self.dic_regionstandard_notaccepted, dic_tempor[i[cnt]])
                            if t != None:
                                for n in self.dic_regionstandard:
                                    if n == t:
                                        self.dic_region[n].append(i[cnt])
                                        self.dic_regionstandard[n] = self.add_region(self.dic_regionstandard[n], dic_tempor[i[cnt]])
                                        self.dic_regionstandard_notaccepted[n] = self.add_region(self.dic_regionstandard[n], dic_tempor[i[cnt]])
                            else:
                                ls2 = []
                                ls2.append(i[cnt])
                                self.Region.append(ls2)
                                self.notaccepted.append(ls2)
                                self.cnt += 1
                                self.dic_region[self.cnt] = ls2
                                self.dic_regionstandard[self.cnt] = dic_tempor[i[cnt]]
                                self.dic_regionstandard_notaccepted[self.cnt] = dic_tempor[i[cnt]]
                            for m in self.dic_region:
                                if i[cnt] in self.dic_region[m]:
                                    self.dic_region[m].remove(i[cnt])
                                    break
                        else:
                            cnt += 1
            self.flag_notaccepted = 0               
            if self.flag_notaccepted == 0:
                ls20 = self.less_ls(self.Region,self.notaccepted)
                for i in ls20:             #遍历每一个分区
                    dic_tempor = {}
                    for j in i:                   #遍历分区中的每一个状态
                        ls1 = []
                        for index in range(len(ls)):
                            ls0 = []
                            ls0.append(self.get_goal(ls[index], move, j, dic1, self.dic_region))
                            ls1.append(ls0)
                        dic_tempor[j] = ls1
                        if j == i[0] :
                            for x in self.dic_region:
                                if i == self.dic_region[x]:
                                    self.dic_regionstandard[x] = ls1
                                    self.dic_regionstandard_accepted[x] = ls1
                    cnt = 0
                    while cnt<len(i):
                        if self.is_equal(dic_tempor[i[cnt]],dic_tempor[i[0]]) == 0:
                            self.flag = 1
                            t = self.is_inotherregion(self.dic_regionstandard_accepted, dic_tempor[i[cnt]])
                            if t != None:
                                for n in self.dic_regionstandard:
                                    if n == t:
                                        self.dic_region[n].append(i[cnt])
                                        self.dic_regionstandard[n] = self.add_region(self.dic_regionstandard[n], dic_tempor[i[cnt]])
                                        self.dic_regionstandard_accepted[n] = self.add_region(self.dic_regionstandard[n], dic_tempor[i[cnt]])
                                        
                            else:
                                ls2 = []
                                ls2.append(i[cnt])
                                self.Region.append(ls2)
                                self.accepted.append(ls2)
                                self.cnt += 1
                                self.dic_region[self.cnt] = ls2
                                self.dic_regionstandard[self.cnt] = dic_tempor[i[cnt]]
                                self.dic_regionstandard_accepted[self.cnt] = dic_tempor[i[cnt]]
                            for m in self.dic_region:
                                if i[cnt] in self.dic_region[m]:
                                    self.dic_region[m].remove(i[cnt])
                                    break
                        else:
                            cnt += 1
                self.flag_notaccepted = 1
        self.accepted1,self.notaccepted1 = self.trans_second(self.accepted, self.notaccepted)

                
    def print_ans(self):
        print(self.dic_region)
    def less_ls(self,ls1,ls2):
        ls = []
        ls = ls1[:]
        for i in ls2:
            for j in ls:
                if tuple(j) == tuple(i):
                    ls.remove(j)
        return ls

                
    def get_goal(self,char,move,state,dic1,dic_goal):          #dic_goal是状态分表
        cnt = 0
        cnt1 = 0
        cnt2 = 0
        for i in move:
            if i.get(state) != None:
                cnt1 += 1
                dic = i.get(state)
                if dic.get(char) != None:
                    for j in dic_goal:
                        if dic.get(char) in dic_goal[j]:
                            return j
                else:
                    cnt2 += 1
            else:
                cnt += 1
        if cnt == len(move):
            return -1
        if cnt1 == cnt2:
            return -1
    def is_inotherregion(self,dic_regionstandard,ls):        #分出去的分区是否在已经分好的分区
        dic = self.trans(dic_regionstandard)
        for i in dic:
            ls1 = []
            for j in i:
                ls0 = []
                ls0 = list(j)
                ls1.append(ls0)
            if self.is_equal(ls1, ls)==1:
                return dic[i]
            
    def trans(self,dic_regionstandard):
        dic = {}
        for i in dic_regionstandard.keys():
            ls1 = []
            for j in dic_regionstandard[i]:
                tup = tuple(j)
                ls1.append(tup)
            tu = tuple(ls1)
            dic[tu] = i
        return dic 
    def trans_second(self,accepted,notaccepted):
        accepted1 = []
        notaccepted1 = []
        for t in range(len(accepted)):
            for i in self.dic_region:
                if self.dic_region[i] == accepted[t]:
                    accepted1.append(i)
        for t in range(len(notaccepted)):
            for i in self.dic_region:
                if self.dic_region[i] == notaccepted[t]:
                    notaccepted1.append(i)
        return accepted1,notaccepted1
    def is_equal(self,ls1,ls2):
        flag = 0
        flag1 = 0
        for i in range(len(ls1)):
            if operator.eq(ls2[i],ls1[i]):
                flag1 += 1
            if operator.eq(ls2[i],ls1[i]) and ls2[i] != [-1]:
                for j in range(i):
                    if ls2[j] == [-1]:
                        flag += 1
                for j in range(i+1,len(ls1)):
                    if ls2[j] == [-1]:
                        flag += 1
                if flag == len(ls1) - 1:
                    return 1
                flag = 0
                for j in range(i):
                    if ls1[j] == [-1]:
                        flag += 1
                for j in range(i+1,len(ls1)):
                    if ls1[j] == [-1]:
                        flag += 1
                if flag == len(ls1) - 1:
                    return 1
        if flag1 == len(ls1):
            return 1
        else:
            return 0
    def add_region(self,ls1,ls2):
        for i in range(len(ls1)):
            if ls1[i] == [-1]:
                if ls2[i] != -1:
                    ls1[i] = ls2[i]
        return ls1
        
                           
        

            
        
                        
   

        
        
    
    