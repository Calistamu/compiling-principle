'''
定义优先级
'''
def priority(str):
    dic = {}
    dic[1] = -1
    dic[' '] = -1
    for i in str:
        if i.isalpha():
            dic[i] = 0
        elif i == '+' or i == '-':
            dic[i] = 1
        elif i == '|':
            dic[i] = 2
        elif i == '·' or i == '/':
            dic[i] = 3
        elif i == '*':
            dic[i] = 4
    return dic

# def main():
#     priority("a·b|c·(d*|a)")
# main()