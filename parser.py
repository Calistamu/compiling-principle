import wx 
import wx.xrc 

#------全局变量------#
FIRST = dict()  # FIRST集
FOLLOW = dict()  # FOLLOW集
LAN = dict()  # 文法
Table = dict()  # 分析表
VT = set()  # 终结符
ProcessList = dict()  

class MyFrame1(wx.Frame):    
    def __init__(self, parent):        
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"LL(1)分析器 By Chao", pos=wx.DefaultPosition,                          
        size=wx.Size(460, 327), style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL, name=u"Main")        
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)        
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))        
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))         
        
        bSizer1 = wx.BoxSizer(wx.VERTICAL)         
        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)        
        fgSizer2.SetFlexibleDirection(wx.BOTH)        
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)         
        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"请选择文法文件的位置", wx.DefaultPosition, wx.DefaultSize, 0)        
        self.m_staticText3.Wrap(-1)        
        self.m_staticText3.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString))         
        fgSizer2.Add(self.m_staticText3, 0, wx.ALL, 5)         
        self.m_filePicker1 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",                                               
        wx.DefaultPosition, wx.Size(300, -1),                                               
        wx.FLP_DEFAULT_STYLE | wx.FLP_SMALL)        
        fgSizer2.Add(self.m_filePicker1, 0, wx.ALL, 5)         
        bSizer1.Add(fgSizer2, 0, wx.EXPAND, 5)         
        fgSizer4 = wx.FlexGridSizer(0, 3, 0, 0)        
        fgSizer4.SetFlexibleDirection(wx.BOTH)        
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)         
        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"请输入要分析的字符串", wx.DefaultPosition, wx.DefaultSize, 0)        
        self.m_staticText4.Wrap(-1)        
        fgSizer4.Add(self.m_staticText4, 0, wx.ALL, 5)         
        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1), wx.Size(200, -1), 0)        
        str = self.m_textCtrl3.GetValue()         
        fgSizer4.Add(self.m_textCtrl3, 0, wx.ALL, 5)         
        self.m_button3 = wx.Button(self, wx.ID_ANY, u"分析", wx.DefaultPosition, wx.DefaultSize, 0)        
        fgSizer4.Add(self.m_button3, 0, wx.ALL, 5)         
        bSizer1.Add(fgSizer4, 0, wx.EXPAND, 5)         
        fgSizer5 = wx.FlexGridSizer(0, 1, 0, 0)        
        fgSizer5.SetFlexibleDirection(wx.BOTH)        
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)         
        self.m_ListCtrl1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT, size=wx.Size(445, 210))        
        self.m_ListCtrl1.InsertColumn(0, "分析栈")        
        self.m_ListCtrl1.InsertColumn(1, "剩余输入串")        
        self.m_ListCtrl1.InsertColumn(2, "所用产生式")        
        self.m_ListCtrl1.InsertColumn(3, "动作")        
        fgSizer5.Add(self.m_ListCtrl1, 0, wx.ALL, 5)         
        bSizer1.Add(fgSizer5, 0, wx.EXPAND, 5)         
        self.SetSizer(bSizer1)        
        self.Layout()         
        self.Centre(wx.BOTH)        
        self.m_button3.Bind(wx.EVT_BUTTON, self.m_button3OnButtonClick)     
    def __del__(self):        
        pass     
    def get_lan(self):        
        file_path = self.m_filePicker1.GetPath()        
        fo = open(file_path, "r")  # 读文法文件        
        for line in fo.readlines():            
            splitlist = line[3:].replace("\n", "").split("|")            
            LAN[line[0]] = splitlist     
    def get_first(self):        
        for k in LAN:            
            l = LAN[k]            
            FIRST[k] = list()            
            for s in l:                
                if not (s[0].isupper()):                    
                    FIRST[k].append(s[0])        
        for i in range(2):            
            for k in LAN:                
                l = LAN[k]                
                for s in l:                    
                    if (s[0].isupper()):                        
                        FIRST[k].extend(FIRST[s[0]])                        
                        FIRST[k] = list(set(FIRST[k]))  # 去重        
        print("文法为：%s" % LAN)        
        print("FIRST集为：%s" % FIRST)     
    def get_follow(self):        
        condition = lambda t: t != 'ε'  # 过滤器用于过滤空串        
        for k in LAN:  # 新建list            
            FOLLOW[k] = list()            
            if k == list(LAN.keys())[0]:                
                FOLLOW[k].append('#')        
        for i in range(2):            
            for k in LAN:                
                l = LAN[k]                
                for s in l:                    
                    if s[len(s) - 1].isupper():                        
                        FOLLOW[s[len(s) - 1]].extend(FOLLOW[k])  # 若A→αB是一个产生式，则把FOLLOW(A)加至FOLLOW(B)中                        
                        FOLLOW[s[len(s) - 1]] = list(filter(condition, FOLLOW[s[len(s) - 1]]))  # 去除空串                    
                    for index in range(len(s) - 1):                        
                        if s[index].isupper():                            
                            if s[index + 1].isupper():  # 若A→αBβ是一个产生式，则把FIRST(β)\{ε}加至FOLLOW(B)中；                                
                                FOLLOW[s[index]].extend(FIRST[s[index + 1]])                                
                                FOLLOW[s[index]] = list(filter(condition, FOLLOW[s[index]]))  # 去除空串                            
                            if not (s[index + 1].isupper()) and (s[index + 1] != 'ε'):                                
                                FOLLOW[s[index]].append(s[index + 1])                            
                            emptyflag = 1                            
                            for i in range(index + 1, len(s)):                                
                                if not (s[i].isupper()) or (s[i].isupper() & ('ε' not in FIRST[s[i]])):                                    
                                    emptyflag = 0                                    
                                    break                            
                                if emptyflag == 1:                                
                                    FOLLOW[s[index]].extend(FOLLOW[k])  # A→αBβ是一个产生式而(即ε属于FIRST(β))，则把FOLLOW(A)加至FOLLOW(B)中                                
                                    FOLLOW[s[index]] = list(filter(condition, FOLLOW[s[index]]))  # 去除空串        
        for k in FOLLOW:  # 去重            
            FOLLOW[k] = list(set(FOLLOW[k]))        
        print('FOLLOW集为：%s' % FOLLOW)     
    def get_VT(self):        
        VT.add('#')        
        for l in LAN.values():            
            for s in l:                
                for c in s:                    
                    if not (c.isupper()) and (c != 'ε'): VT.add(c)        
        print('终结符为：%s' % VT)     
    def generate_table(self):        
        self.get_VT()        
        for k in LAN:  # 初始化分析表            
            Table[k] = dict()            
            for e in VT:                
                Table[k][e] = None        
        for k in LAN:            
            l = LAN[k]            
            for s in l:                
                if s[0].isupper():                    
                    for e in VT:                        
                        if e in FIRST[s[0]]: Table[k][e] = s                
                if s[0] in VT:                    
                    Table[k][s[0]] = s                
                if (s[0].isupper() and ('ε' in FIRST[s[0]])) or (s == 'ε'):
                    for c in FOLLOW[k]:                        
                        Table[k][c] = s        
        print('分析表为：%s' % Table)     
    def analyze(self):        
        inputstr = self.m_textCtrl3.GetValue()  # 输入任意字符串        
        inputstr = inputstr[1:]        
        inputstr = list(inputstr[::-1])        
        print(inputstr)        
        process = list()        
        process.append('#')  # "#"入栈        
        process.append(list(LAN.keys())[0])  # 开始符入栈        
        errorflag = 0  # 出错标识        
        count = 0  # 插入列表时的索引        
        ProcessList.clear()        
        ProcessList[count] = (''.join(process), ''.join(inputstr), ' ', '初始化')        
        while True:            
            count+=1            
            current = process.pop()            
            if current == inputstr[-1] == '#':  # 分析成功结束                
                ProcessList[count] = ('√', '√', '恭喜你', '成功')                
                break;             
            if (current in VT) and (current == inputstr[-1]):  # 遇到终结符                
                inputstr.pop()                
                ProcessList[count] = (''.join(process), ''.join(inputstr), ' ', 'GETNEXT')                
                continue             
            if inputstr[-1] in VT:  # 判断是不是终结符                
                new = Table[current][inputstr[-1]]            
            else:                
                errorflag = 1                
                ProcessList[count] = (''.join(process), ''.join(inputstr), ' ', 'Error:输入不合法！')                
                break             
            if (new == None):  # 没有找到对应产生式                
                errorflag = 1                
                ProcessList[count] = (''.join(process), ''.join(inputstr), ' ', 'Error:没有找到对应产生式!')                
                break             
            if (new == 'ε'):  # 产生式为空串                
                ProcessList[count] = (''.join(process), ''.join(inputstr), current+'->ε', 'POP')                
                continue             
            for c in reversed(new):  # 将产生式入栈                
                process.append(c)            
            ProcessList[count] = (''.join(process), ''.join(inputstr), current+'->'+''.join(new), 'POP,PUSH')         
        
        if errorflag == 0:            
            print("分析成功！")        
        else:            
            print("分析失败！")          
                    
        items = ProcessList.items()        
        self.m_ListCtrl1.DeleteAllItems()        
        for key, data in items:            
            index = self.m_ListCtrl1.InsertItem(self.m_ListCtrl1.GetItemCount(), str(key))            
            self.m_ListCtrl1.SetItem(index, 0, data[0])            
            self.m_ListCtrl1.SetItem(index, 1, data[1])            
            self.m_ListCtrl1.SetItem(index, 2, data[2])            
            self.m_ListCtrl1.SetItem(index, 3, data[3])            
            self.m_ListCtrl1.SetColumnWidth(0, 80)            
            self.m_ListCtrl1.SetColumnWidth(1, 80)            
            self.m_ListCtrl1.SetColumnWidth(2, 100)            
            self.m_ListCtrl1.SetColumnWidth(3, 175)     
    def m_button3OnButtonClick(self, event):        
            self.get_lan()  # 得到文法        
            self.get_first()  # 得到FIRST集        
            self.get_follow()  # 得到FOLLOW集s        
            self.generate_table()  # 得到分析表        
            self.analyze()  # 对输入字符串进行分析  
if __name__ == '__main__':    
    app = wx.App(False)    
    frame = MyFrame1(None)    
    frame.Show(True)    
    app.MainLoop()
