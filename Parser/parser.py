#!/usr/env python
# -*- coding: UTF-8 -*-
"""
 文法：
    E->E+T | T
    T->T*F | F
    F->(E)|i
 消除左递归：
    E->TH
    H->+TH|e(一普赛肋)
    T->FY
    Y->*FY|e
    F->(E)|i
 非终结符：
    E，H，T，Y，F
 终结符:
    i,+,*,(,),#
"""
# 手动构造预测分析表
dists = {
    ('E', 'i'): 'TH',
    ('E', '('): 'TH',
    ('H', '+'): '+TH',
    ('H', ')'): 'e',
    ('H', '#'): 'e',
    ('T', 'i'): 'FY',
    ('T', '('): 'FY',
    ('Y', '+'): 'e',
    ('Y', '*'): '*FY',
    ('Y', ')'): 'e',
    ('Y', '#'): 'e',
    ('F', 'i'): 'i',
    ('F', '('): '(E)',
}

# 构造终结符集合
Vt = ('i', '+', '*', '(', ')')

# 构造非终结符集合
Vh = ('E', 'H', 'T', 'Y', 'F')


# 获取输入栈中的内容
def printstack(stack):
    rtu = ''
    for i in stack:
        rtu += i
    return rtu


# 得到输入串剩余串
def printstr(str, index):
    rtu = ''
    for i in range(index, len(str), 1):
        rtu += str[i]
    return rtu


# 定义error函数
def error():
    print('Error')
    exit()


# 总控程序
def masterctrl(str):
    '''
    总控程序，用于进程文法的判断
    '''
    # 用列表模拟栈
    stack = []
    location = 0
    # 将#号入栈
    stack.append(str[location])

    # 将文法开始符入栈
    stack.append('E')
    # 将输入串第一个字符读进a中
    location += 1
    a = str[location]
    printstack(stack)
    flag = True
    count = 0
    print('%d\t\t%s\t\t%s' % (count, printstack(stack), printstr(str, location)))
    while flag:
        if count == 0:
            pass
        else:
            if x in Vt:
                print('%d\t\t%s\t\t%s' % (count, printstack(stack), printstr(str, location)))
            else:
                print('%d\t\t%s\t\t%s\t\t%s->%s' % (count, printstack(stack), printstr(str, location), x, s))
        x = stack.pop()
        if x in Vt:
            if x == str[location]:
                location += 1
                a = str[location]
            else:
                error()
        elif x == '#':
            if x == a:
                flag = False
            else:
                error()
        elif (x, a) in dists.keys():
            s = dists[(x, a)]
            for i in range(len(s) - 1, -1, -1):
                if s[i] != 'e':
                    stack.append(s[i])
        else:
            error()
        count += 1


def main():
    # str = input()
    str = '#i*i+i#'
    print("步骤\t\t符号栈\t\t输入串\t\t\t所用产生式")
    masterctrl(str)


if __name__ == '__main__':
    main()