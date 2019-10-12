'''
实现NFA的Closure闭包运算及move运算以及获取NFA的列表，move列表
'''

from stack import Stack
from retoNFA import *
class Nfa:
    def __init__(self, start,accepted,move):
        self.start = start
        self.accepted = accepted
        self.move = move
    #进行闭包运算,ls为状态集，u为ls状态集的闭包
    def make_Closure(self,ls):
        u = []
        ls_mid = []
        stack = Stack()
        for i in ls:                             #先把状态集全部压入栈
            stack.push(i)
            u.append(i)
        while not(stack.is_empty()):
            i = stack.pop()                          #取出栈顶元素
            for d in self.move:                      #遍历状态表，如果存在空符号，则压入栈
                if d.get(i) != None:
                    if 'ε' in d.get(i):
                        a = d.get(i)['ε']
                        if a not in ls_mid and a not in u:
                            stack.push(a)
                            ls_mid.append(a)
                            u.append(a)
                    else:
                        pass
        return u
    #make_move方法求子集，ls为初态集，char为转换字符，u为转换后的集合
    def make_move(self,ls,char):
        u = []
        for i in ls:
            for d in self.move:
                if d.get(i) != None:
                    if char in d.get(i):
                        a = d.get(i)[char]
                        if a not in u:
                            u.append(a)
#                     elif 'ε' in d.get(i):
                        
        return u
    #获得NFA的开始状态，结束状态，以及move列表
    def get_startendmove(self,ls):
        return retoNFA(ls)
    #获得NFA的字母列表
    def get_alpha(self,ls):
        ls1 = []
        for i in ls:
            if i.isalpha() and i not in ls1:
                ls1.append(i)
        return ls1
        