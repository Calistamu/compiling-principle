from collections import defaultdict

def addtwodimdict(thedict, key_a, key_b, val):     
    if key_a in thedict:        
        thedict[key_a].update({key_b: val})    
    else:        
        thedict.update({key_a:{key_b: val}})  

def GetFirst(stack_item):    
    if stack_item[1] in vt:#产生式第一个为终结        
        first[stack_item[0]].add(stack_item[1])#将其放入第一个的first    
    else:        
        for find_item in stack:            
            if find_item[0]==stack_item[1]:                
                GetFirst(find_item)                
                first[stack_item[0]]=first[stack_item[1]]|first[stack_item[0]] 

def GetFollow(vi_item):    
    for i in stack:        
        j=1        
        while j<len(i)-1:            
            if (i[j]==vi_item)&(i[j+1] in vt): # 存在 Ab 则把b放入                
                follow[vi_item].add(i[j+1])            
            if (i[j]==vi_item)&(i[j+1] in vi): #存在AB 则把B的first放入                
                follow[vi_item]=follow[vi_item]|first[i[j+1]]-{'ε'}            
            if (i[j] in vi)&('ε' in first[i[j+1]]): #存在 A=EBC 且C的first中有空                
                follow[i[j]]=follow[i[0]]|follow[i[j]]            
            j+=1        
        if i[len(i)-1] ==vi_item:#为某行最后一个字符            
            follow[vi_item].add('$')          
        if (i[0]==vi_item)&(i[len(i)-1] in vi):#A=....B            
            follow[i[len(i)-1]]=follow[vi_item]|follow[i[len(i)-1]]        
        if (i[len(i)-1]==vi_item)&(i[0] in vi):            
            follow[vi_item]=follow[i[0]]|follow[i[len(i)-1]]                 

vt=['i','+','*','(',')','ε'] #终结字符
vi=['E','e','T','t','F'] #非终结字符
gramma=open('C:/Users/karen/Documents/GitHub/compiling-principle/test.txt').readlines()
stack=[]
for i in gramma:    
    ss=i[0:1]    
    j=0    
    while j<len(i):        
        if i[j]=='>':            
            break        
        j+=1    
    j+=1 #找到->后的第一个位置    
    while j<len(i):        
        if i[j]=='\n':            
            break        
        if i[j]!='|':            
            ss+=i[j]        
        else:            
            stack.append(ss)            
            ss=i[0:1]        
        j+=1    
    stack.append(ss)
first=defaultdict(set) #构建元素映射到多个元素（集合）的字典
follow=defaultdict(set)
for stack_item in stack:    
    GetFirst(stack_item)    

follow['E'].add('$')   
for vi_item in vi:    
    GetFollow(vi_item)
ana_table=dict() #建立预测分析表 其中key为非终结符和输入符号字符串的相连接 value为对应的分析结果  

addtwodimdict(ana_table, 'E', 'i', 'E->Te')
addtwodimdict(ana_table, 'E', '(', 'E->Te')
addtwodimdict(ana_table, 'e', '+', 'e->+Te')
addtwodimdict(ana_table, 'e', ')', 'e->ε')
addtwodimdict(ana_table, 'e', '$', 'e->ε')
addtwodimdict(ana_table, 'T', 'i', 'T->Ft')
addtwodimdict(ana_table, 'T', '(', 'T->Ft')
addtwodimdict(ana_table, 't', '+', 't->ε')
addtwodimdict(ana_table, 't', '*', 't->*Ft')
addtwodimdict(ana_table, 't', ')', 't->ε')
addtwodimdict(ana_table, 't', '$', 't->ε')
addtwodimdict(ana_table, 'F', 'i', 'F->i')
addtwodimdict(ana_table, 'F', ')', 'F->(E)')     

sen="i*i+i$"
ip=0 
ss=['$','E']
while ss[len(ss)-1]!='$':    
    print(ss)    
    print(sen[ip])    
    if ss[len(ss)-1]==sen[ip]:        
        ss.pop()        
        ip+=1    
    elif ss[len(ss)-1] in vt:        
        print("error1")        
        break    
    elif sen[ip] not in ana_table[ss[len(ss)-1]]:        
        print("error2")        
        break    
    elif sen[ip] in ana_table[ss[len(ss)-1]]:        
        strings=ana_table[ss[len(ss)-1]][sen[ip]]        
        print(strings)        
        ss.pop()        
        j=len(strings)-1        
        while j>2:            
            if strings[j]!='ε':                
                ss.append(strings[j])            
            j-=1
