# 用于输入任意正规式，输出NFA、DFA、DFA最小化的图片

## py功能介绍
 
stack.py---定义栈结构  
priority---定义符号优先级 
main.py----程序启动   
re.py------从字母表到逆波兰式  

* 1.改写正则表达式，符号之间添加连接符  
* 2.中缀表达式转后缀表达式，去掉"("和")"

retoNFA.py---逆波兰式到NFA  

* 调用ClosureAndMove.py实现NFA的Closure闭包运算及move运算以及获取NFA的列表，move列表

ClosureAndMove.py---NFA的闭包和move运算    
NFAtoDFA.py---NFA到DFA  
DFAtoMDFA.py---DFA到最小化DFA  
Graphsum.py----画图
* graphviz的环境变量报错，重新安装下载，先系统安装，再Python安装

## 小组分工
结合小组成员的优缺点组队
chao---负责主要代码
* 对理论知识的理解特别慢
han---理论讲解
* 理论知识学习很强，但是敲代码不行
wu---专调各种各样的Bug
* 长期小组合作，chao出现各种Bug,wu总能跑通

## 不足
老师要求的是面向用户的程序，想使用flask做成web程序，用户可以任意输入正规式，或给出NAF、DFA，在网页上显示输出结果，但是没有实现。