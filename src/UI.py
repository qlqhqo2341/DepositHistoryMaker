# -*- coding:utf-8 -*-
import wx
import store
import printer
import wx.grid as gridlib

class StartForm(wx.Frame):
    def __init__(self, main, *args, **kwargs):
        super(StartForm, self).__init__(*args, **kwargs)
        self.main = main
        self.createControl()
        self.bindEvents()
        self.doLayout()

    def newFile(self,evt):
        self.main.newFile()
        self.main.Show()
        self.Hide()

    def load(self,evt):
        store.dialogLoad()
        self.main.Show()
        self.Hide()

    #Widgets
    def createControl(self):
        size = (200,300)
        self.NewFileButton = wx.Button(self, label='새 파일',size=size)
        self.LoadButton = wx.Button(self, label='불러오기',size=size)

    def bindEvents(self):
        self.NewFileButton.Bind(wx.EVT_BUTTON, self.newFile)

    def doLayout(self):
        box = wx.BoxSizer()
        box.AddMany((self.NewFileButton, self.LoadButton))
        self.SetSizerAndFit(box)


class MainForm(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        self.firstForm = StartForm(self,None,-1,args[2])
        self.createControl()
        self.bindEvents()
        self.doLayout()
        self.firstForm.Show()

    def newFile(self, path=None):
        store.init()
        self.refresh()

    def refresh(self):
        data = store.dhData
        history_size, undoCount = store.history_size, store.undoCount

        # TODO : according to widget. setting data    

    def closing(self, evt):
        
        self.Hide()
        self.firstForm.Show()

    #widgets
    def createControl(self):
        self.sums = ['날짜별 합계','행사별 합계','총 합계']
        self.sheet = gridlib.Grid(self)
        self.sheet.CreateGrid(10,5)
        
        for ind,name in enumerate(['날짜','행사','내용','수입',
        '지출']):
            self.sheet.SetColLabelValue(ind,name)

                            
        self.buttons = [
            ( wx.Button(self, label="새 파일"),
            wx.Button(self, label="불러오기")),
            wx.Button(self,label="저장하기"),
            wx.Button(self,label="내용 추가"),
            ( wx.Button(self, label="삭제"),
            wx.Button(self, label="수정")),
            ( wx.Button(self, label="되돌리기"),
            wx.Button(self, label="다시실행")),
            wx.Button(self, label="프린트")
        ]

        self.checks = []
        for i in self.sums:
            self.checks.append(wx.CheckBox(self,label=i))

    def bindEvents(self):
        buttonEvents = {
            "새 파일":(wx.EVT_BUTTON,None)
        }
        self.Bind(wx.EVT_CLOSE,self.closing)     

    def doLayout(self):
        self.divider = wx.BoxSizer()
        left, right = wx.BoxSizer(orient=wx.VERTICAL), wx.BoxSizer(orient=wx.VERTICAL)
        
        left.Add(self.sheet, flag=wx.EXPAND)
        box = wx.BoxSizer()
        box.AddMany(self.checks)
        left.Add(box, flag=wx.EXPAND)

        # right buttons add
        for but in self.buttons:
            if isinstance(but,tuple):
                double = wx.BoxSizer()
                double.AddMany(but)
                right.Add(double)
            else:
                right.Add(but,flag=wx.EXPAND)
        self.divider.Add(left)
        self.divider.Add(right,flag=wx.EXPAND)
        self.SetSizerAndFit(self.divider)  

# UI Test Code!
if __name__ == "__main__":
    app = wx.App(0)
    main = MainForm(None, -1, "Hi!")
    app.MainLoop()
    