# -*- coding:utf-8 -*-
import wx
import store
import printer
import operator
import wx.grid as gridlib

def moneyStr(money):
    v,c,m = money,0,False
    r = ""
    if v<0:
        v,m=-v,True
    while v!=0:
        digit=v%10
        r = str(digit) + r
        c+=1
        v=v//10
        if c==3 and v!=0:
            r = ',' + r
            c=0
    r = ('-' if m else '') + r
    return r


class StartForm(wx.Frame):
    def __init__(self, main, *args, **kwargs):
        super(StartForm, self).__init__(*args, **kwargs)
        self.main = main
        self.createControl()
        self.bindEvents()
        self.doLayout()

    def newFile(self,evt):
        store.init(self.main)
        self.main.Show()
        self.Hide()

    def load(self,evt):
        self.Hide()
        self.main.Show()
        store.dialogLoad()

    #Widgets
    def createControl(self):
        size = (200,300)
        self.NewFileButton = wx.Button(self, label='새 파일',size=size)
        self.LoadButton = wx.Button(self, label='불러오기',size=size)

    def bindEvents(self):
        self.NewFileButton.Bind(wx.EVT_BUTTON, self.newFile)
        self.LoadButton.Bind(wx.EVT_BUTTON, self.load)

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

        store.init(self)

    def refresh(self):
        data = sorted(store.dhData.items(), key=operator.itemgetter(0))
        history_size, undoCount = store.history_size, store.undoCount
        sheet=self.sheet
        # TODO : check combobox. make the right summation and SORT
        
        remain=0
        sheet.ClearGrid()
        for ind, tup in enumerate(data):
            k,v=tup
            for ind2,val in enumerate(k):
                sheet.SetCellValue(ind, ind2, val)
            remain += v
            val = (moneyStr(v),"0",moneyStr(remain)) if v>0 else ("0", moneyStr(-v),moneyStr(remain))
            for ind2,v in enumerate(val):
                sheet.SetCellValue(ind,ind2+3,v)
        if len(store.activityData)-undoCount==0:
            # can not undo
            self.butUndo.Disable()
        else:
            self.butUndo.Enable()

    def getSelectedRows(self):
        # TODO : http://ginstrom.com/scribbles/2008/09/07/getting-the-selected-cells-from-a-wxpython-grid/
        # Get Rows!!
        pass

    #event Methods
    def onLoad(self, evt):
        store.init()
        store.dialogLoad()

    def onSave(self, evt):
        store.dialogSave()
    
    def onNewFile(self, evt):
        if evt!=None and store.is_saved==False:
            if store.dialogNotSaving() == wx.ID_CANCEL:
                return
        store.init(self)
        self.SetTitle("입출금내역 작성기")
        self.refresh()

    def onClose(self, evt):
        if not store.is_saved:
            r = store.dialogNotSaving() 
            if r== wx.ID_CANCEL:
                return
            elif r == wx.ID_OK:
                store.dialogSave()
        self.Hide()
        self.firstForm.Show()

    def onCheckSum(self, evt):
        self.refresh()

    def onAdd(self, evt):
        pass

    def onRemove(self,evt):
        pass
        
    
    def onModify(self,evt):
        pass
        

    #widgets
    def createControl(self):
        self.sums = ['날짜별 합계','행사별 합계','총 합계']
        self.sheet = gridlib.Grid(self)
        self.sheet.CreateGrid(10,6)
        
        for ind,name in enumerate(['날짜','행사','내용','수입',
        '지출','잔액']):
            self.sheet.SetColLabelValue(ind,name)
        self.sheet.SetRowLabelSize(0)
        self.sheet.EnableEditing(False)
        self.sheet.DisableDragGridSize()

        self.butNew = wx.Button(self, label="새 파일")
        self.butLoad = wx.Button(self, label="불러오기")
        self.butSave = wx.Button(self,label="저장하기")
        self.butAdd = wx.Button(self,label="내용 추가")
        self.butDel = wx.Button(self,label="삭제")
        self.butMod = wx.Button(self,label="수정")
        self.butUndo = wx.Button(self,label="되돌리기")
        self.butRedo = wx.Button(self,label="다시실행")
        self.butPrint = wx.Button(self,label="프린트")
        self.buttons = [
            (self.butNew, self.butLoad),
            self.butSave,self.butAdd,
            (self.butDel,self.butMod),
            (self.butUndo,self.butRedo),
            self.butPrint
        ]


        self.checks = []
        for i in self.sums:
            self.checks.append(wx.CheckBox(self,label=i))

    def bindEvents(self):
        evts = [
            (self, wx.EVT_CLOSE,self.onClose),
            (self.butNew, wx.EVT_BUTTON, self.onNewFile),
            (self.butSave, wx.EVT_BUTTON, store.dialogSave),
            (self.butLoad, wx.EVT_BUTTON, store.dialogLoad),
            (self.butAdd, wx.EVT_BUTTON, self.onAdd),
            (self.butDel, wx.EVT_BUTTON, self.onRemove),
            (self.butMod, wx.EVT_BUTTON, self.onModify)
        ]
        for control, evt, func in evts:
            control.Bind(evt,func)

        for checkbox in self.checks:
            checkbox.Bind(wx.EVT_CHECKBOX,self.onCheckSum)
        

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
    main = MainForm(None, -1, "입출금내역 작성기")
    app.MainLoop()
    