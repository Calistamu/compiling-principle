"""
从字母表到逆波兰表达式
"""

from stack import Stack
from priority import priority
from inspect import stack

#构建字母表如：ab|c(d*|a),添加乘法点->a·b|c·(d*|a)
def add_sign(str):
    ls = list(str)+['!']
    length = len(ls)
    i = 0
    while ls[i] != '!':
        if ls[i].isalpha() and ls[i+1].isalpha():
            ls.insert(i+1, "·")
            i += 1
        if ls[i].isalpha() and ls[i+1] == "(":
            ls.insert(i+1,"·")
            i += 1
        if ls[i] == ")" and ls[i+1].isalpha():
            ls.insert(i+1,"·")
            i += 1
        if ls[i] == "*" and ls[i+1].isalpha():
            ls.insert(i+1,"·")
            i += 1
        if ls[i] == ")" and ls[i+1] == "(":
            ls.insert(i+1,"·")
            i += 1
        if ls[i] == "*" and ls[i+1] == "(":
            ls.insert(i+1,"·")
            i += 1
        i += 1
    del ls[-1]
    newstr = ''.join(ls)
    return newstr

#用调度场算法实现由中缀表达式到逆波兰表达式
def shunting_yard(str):
    stack_sign = Stack()
    stack_sign.push(1)
    str_add_sign = add_sign(str)
    dic_priority = priority(str_add_sign)
    ls = []
    for i in str_add_sign:
        if i.isalpha():
            ls.append(i)
        else:
            if i == '(':
                stack_sign.push(i)
            elif i == ')':
                a = stack_sign.pop()
                while True:
                    if a != '(':
                        ls.append(a)
                        a = stack_sign.pop()
                    else:
                        break
            else:
                if stack_sign.peek() == '(':
                    stack_sign.push(i)
                elif dic_priority[stack_sign.peek()] >= dic_priority[i]:
                    b = stack_sign.pop()
                    ls.append(b)
                    if stack_sign.peek() == '(':
                        stack_sign.push(i)
                    else:
                        while dic_priority[stack_sign.peek()] >= dic_priority[i]:
                            b = stack_sign.pop()
                            ls.append(b)
                        stack_sign.push(i)
                else:
                    stack_sign.push(i)
    c = stack_sign.pop()
    while c!=1:
        ls.append(c)
        c = stack_sign.pop()
    return ls
                
                    
                    

        
            
    
    
    
            