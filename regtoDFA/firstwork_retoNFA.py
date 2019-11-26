'''
从逆波兰表达式到NFA
'''
from firstwork_stack import Stack
from firstwork_re import *

class State:
    def __init__(self,ID,start = None,accepted = None):
        self.ID = ID
        self.start = start
        self.accepted = accepted
        
class Transition:
    def __init__(self,sourcestate,targetstate,char = 'ε'):
        self.sourcestate = sourcestate
        self.targetstate = targetstate
        self.char = char
        
    def print_side(self):
        print("{0}-->{1},值：{2}".format(self.sourcestate.ID, self.targetstate.ID,self.char))
              
def make_begin():
    start = State('start')
def make_ls_state(ls_state,k,values,state):   #ls_state为move列表
    dic = {}
    dic1 = {}
    dic1[values] = state.ID
    dic[k] = dic1
    ls_state.append(dic)
def is_alpha(k,cnt_State,values,ls_state):
    a = State(k)
    b = State(k+1)
    make_ls_state(ls_state, k, values, b)
    side = Transition(a,b,values)
    side.print_side()
    return State(cnt_State,a,b),ls_state
def is_or(k,cnt_State,state1,state2,ls_state):
    a = State(k)
    b = State(k+1)
    make_ls_state(ls_state, k, 'ε', state1.start)
    s1 = Transition(a,state1.start)
    s1.print_side()
    make_ls_state(ls_state, k,'ε' , state2.start)
    s2 = Transition(a,state2.start)
    s2.print_side()
    make_ls_state(ls_state, state1.accepted.ID, 'ε', b)
    s3 = Transition(state1.accepted,b)
    s3.print_side()
    make_ls_state(ls_state, state2.accepted.ID, 'ε', b)
    s4 = Transition(state2.accepted,b)
    s4.print_side()
    return State(cnt_State,a,b),ls_state
def is_and(k,cnt_State,state1,state2,ls_state):
    a = State(k)
    b = State(k+1)
    make_ls_state(ls_state, k, 'ε', state1.start)
    s1 = Transition(a,state1.start)
    s1.print_side()
    make_ls_state(ls_state, state1.accepted.ID, 'ε', state2.start)
    s2 = Transition(state1.accepted,state2.start)
    s2.print_side()
    make_ls_state(ls_state, state2.accepted.ID, 'ε', b)
    s3 = Transition(state2.accepted,b)
    s3.print_side()
    return State(cnt_State,a,b),ls_state
def is_repeat(k,cnt_State,state1,ls_state):
    a = State(k)
    b = State(k+1)
    make_ls_state(ls_state,k, 'ε', state1.start)
    s1 = Transition(a,state1.start)
    s1.print_side()
    make_ls_state(ls_state,state1.accepted.ID, 'ε', state1.start)
    s2 = Transition(state1.accepted,state1.start)
    s2.print_side()
    make_ls_state(ls_state,state1.accepted.ID, 'ε', b)
    s3 = Transition(state1.accepted,b)
    s3.print_side()
    make_ls_state(ls_state,k, 'ε', b)
    s4 = Transition(a,b)
    s4.print_side()
    return State(cnt_State,a,b),ls_state 
def retoNFA(ls):
    stack_NFA = Stack()
    dic_side = {}
    cnt_state = 1
    cnt_State = 1
    ls_state = []
    for i in ls:
        if i.isalpha():
            state,ls_state = is_alpha(cnt_state,cnt_State, i,ls_state)
            stack_NFA.push(state)
            cnt_state += 2
            cnt_State += 1
        else:
            if i == '*':
                state1 = stack_NFA.pop()
                state,ls_state = is_repeat(cnt_state,cnt_State,state1,ls_state)
                stack_NFA.push(state)
                cnt_state += 2
                cnt_State += 1
            elif i == '|':
                state1 = stack_NFA.pop()
                state2 = stack_NFA.pop()
                state,ls_state = is_or(cnt_state,cnt_State,state2,state1,ls_state) 
                stack_NFA.push(state)
                cnt_state += 2             
                cnt_State += 1   
            elif i == '·':
                state1 = stack_NFA.pop()
                state2 = stack_NFA.pop()
                state,ls_state = is_and(cnt_state,cnt_State,state2,state1,ls_state)
                stack_NFA.push(state)
                cnt_state += 2
                cnt_State += 1
    ans = stack_NFA.pop()
    return ans.start.ID,ans.accepted.ID,ls_state
    
                
                
                 
                
        
            
    