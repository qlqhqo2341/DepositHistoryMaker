# -*- coding:utf-8 -*-
import wx
import store
import printer
import operator
import wx.grid as gridlib
import wx.lib.scrolledpanel as scrolled
from dataForm import DataForm

def moneyStr(money):
    def core(obj):
        v,c,m = obj,0,False
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

    if isinstance(money,list) or isinstance(money,tuple):
        r = []
        for obj in money:
            r.append(moneyStr(obj))
        return r
    else:
        return core(money)

def corners_to_cells(top_lefts, bottom_rights):
    """
    Take lists of top left and bottom right corners, and
    return a list of all the cells in that range
    """
    cells = set()
    for top_left, bottom_right in zip(top_lefts, bottom_rights):

        rows_start = top_left[0]
        rows_end = bottom_right[0]

        rows = range(rows_start, rows_end+1)

        cells=cells.union(rows)

    return cells

def get_selected_cells(grid):
    """
    Return the selected cells in the grid as a list of
    (row, col) pairs.
    We need to take care of three possibilities:
    1. Multiple cells were click-selected (GetSelectedCells)
    2. Multiple cells were drag selected (GetSelectionBlock…)
    3. A single cell only is selected (CursorRow/Col)
    """

    #TODO : need to check and get right data for their combination 
    top_left = grid.GetSelectionBlockTopLeft()

    if top_left:
        bottom_right = grid.GetSelectionBlockBottomRight()
        return corners_to_cells(top_left, bottom_right)

    selection = grid.GetSelectedCells()

    if not selection:
        row = grid.GetGridCursorRow()
        col = grid.GetGridCursorCol()
        return row

    rows=set()
    for cell in selection:
        rows.add(cell.GetRow())

    return rows

class StartForm(wx.Frame):
    def __init__(self, main, *args, **kwargs):
        super(StartForm, self).__init__(*args, **kwargs)
        self.main = main
        self.createControl()
        self.bindEvents()
        self.doLayout()

    def newFile(self,evt):
        store.init(self.main)
        self.main.SetTitle('입출금내역 작성기')
        self.main.Show()
        self.main.Maximize() if not self.main.IsMaximized() else ''
        self.Hide()

    def load(self,evt):
        self.Hide()
        self.main.Show()
        store.dialogLoad()
        self.main.Maximize() if not self.main.IsMaximized() else ''

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
        self.SetBackgroundColour("WHITE")
        self.createControl()
        self.bindEvents()
        self.doLayout()
        self.firstForm.Show()

        store.init(self)

    def refresh(self):
        data = sorted(store.dhData.items(), key=operator.itemgetter(0))
        present = list()
        history_size, undoCount = store.history_size, store.undoCount
        sheet=self.sheet
        postiveAdd = lambda x,y,z: [x+z,y] if z>0 else [x,y-z]
        # TODO : check combobox. make the right summation and SORT
        
        def appendRow(seq):
            sheet.AppendRows()
            ind = sheet.GetNumberRows()
            for i,v in enumerate(seq):
                sheet.SetCellValue(ind-1,i,str(v))
                sheet.SetCellAlignment(ind-1,i,\
                    wx.ALIGN_RIGHT if i>2 else wx.ALIGN_CENTER, wx.ALIGN_CENTER)


        sheet.DeleteRows(numRows=sheet.GetNumberRows()) if sheet.GetNumberRows() > 0 else ''
        sheet.ClearGrid()

        remain = 0
        totalGet, totalPay, dayGet, dayPay,festGet,festPay = 0,0,0,0,0,0
        daySumBool,festSumBool,totalSumBool = [but.GetValue() for but in self.checks]
        # calculate summation before Present data
        for ind, tup in enumerate(data):
            nowKey,nowVal = tup
            nowKey = list(nowKey)
            dayGet,dayPay = postiveAdd(dayGet,dayPay,nowVal)
            if nowKey[1] != '':
                festGet,festPay = postiveAdd(festGet,festPay,nowVal)
            totalGet,totalPay = postiveAdd(totalGet,totalPay,nowVal)
            
            remain += nowVal
            present.append(list(nowKey)+moneyStr(postiveAdd(0,0,nowVal)+[remain]))
            
            #Exist next
            if len(data) != ind+1:
                nextKey,nextVal = data[ind+1]
                if nowKey[0] != nextKey[0]: #Day check
                    present.append(nowKey[0:2]+['All']+moneyStr([festGet,festPay])) \
                        if festSumBool and nowKey[1] != '' else ''
                    present.append(nowKey[0:1]+['All','All']+moneyStr([dayGet,dayPay])) if daySumBool else ''
                    festGet,festPay,dayGet,dayPay=0,0,0,0
                    continue
                if nowKey[1] != nextKey[1] and nowKey[1] != '': #Fest check
                    present.append(nowKey[0:2]+['All']+moneyStr([festGet,festPay])) if festSumBool else ''
                    festGet,festPay=0,0
                    continue                
            #Last tuple
            else:
                present.append(nowKey[0:2]+['All']+moneyStr([festGet,festPay])) \
                    if festSumBool and nowKey[1] != '' else ''
                present.append([nowKey[0],'All','All']+moneyStr([dayGet,dayPay])) if daySumBool else ''
                present.append(['All']*3+moneyStr([totalGet,totalPay])) if totalSumBool else ''

        # present grid table by present list
        for lis in present:
            appendRow(lis)
       
        sheet.AutoSize()
        if len(store.activityData)-undoCount==0:
            # can not undo
            self.butUndo.Disable()
        else:
            self.butUndo.Enable()

    def getSelectedRows(self):
        # TODO : http://ginstrom.com/scribbles/2008/09/07/getting-the-selected-cells-from-a-wxpython-grid/
        # Get Rows!!
        return get_selected_cells(self.sheet)
        

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
        if 'dataForm' in self.__dict__ and self.dataForm:
            self.dataForm.Destroy()
            self.dataForm = None
        self.firstForm.Show()

    def onCheckSum(self, evt):
        self.refresh()

    def onAdd(self, evt):
        if not 'dataForm' in self.__dict__ or not self.dataForm:
            self.dataForm = DataForm(self,'add')
            self.dataForm.Show()
        else:
            self.dataForm.Destroy()
            self.dataForm=None
            self.dataForm = DataForm(self,'add')
            self.dataForm.Show()

    def onRemove(self,evt):
        obj=self.getSelectedRows()
        store.remove(obj)
        
    
    def onModify(self,evt):
        pass
       

    #widgets
    def createControl(self):
        self.sums = ['날짜별 합계','행사별 합계','총 합계']
        self.scrolledSheet = scrolled.ScrolledPanel(self)
        self.sheet = gridlib.Grid(self.scrolledSheet)
        self.sheet.CreateGrid(0,6)
        self.sheet.SetDefaultCellFont(wx.Font(wx.FontInfo(13).Bold()))
        self.sheet.SetDefaultCellAlignment(wx.ALIGN_RIGHT,wx.ALIGN_CENTER)
        
        for ind,name in enumerate(['날짜','행사','내용','수입',
        '지출','잔액']):
            self.sheet.SetColLabelValue(ind,name)
        self.sheet.SetRowLabelSize(0)
        self.sheet.EnableEditing(False)
        self.sheet.DisableDragGridSize()

        size = (100,35)
        self.butNew = wx.Button(self, label="새 파일", size=size)
        self.butLoad = wx.Button(self, label="불러오기", size=size)
        self.butSave = wx.Button(self,label="저장하기", size=size)
        self.butAdd = wx.Button(self,label="내용 추가", size=size)
        self.butDel = wx.Button(self,label="삭제", size=size)
        self.butMod = wx.Button(self,label="수정", size=size)
        self.butUndo = wx.Button(self,label="되돌리기", size=size)
        self.butRedo = wx.Button(self,label="다시실행", size=size)
        self.butPrint = wx.Button(self,label="프린트", size=size)
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
        
        scrollsizer = wx.BoxSizer()
        scrollsizer.Add(self.sheet, 1, wx.EXPAND)
        self.scrolledSheet.SetSizerAndFit(scrollsizer)
        self.scrolledSheet.SetupScrolling()

        left.Add(self.scrolledSheet, 1,flag=wx.EXPAND)
        box = wx.BoxSizer()
        box.AddMany([(b,1,wx.EXPAND) for b in self.checks])
        left.Add(box, 0,flag=wx.EXPAND)

        # right buttons add
        for but in self.buttons:
            if isinstance(but,tuple):
                double = wx.BoxSizer()
                double.AddMany([ (b,1,wx.EXPAND) for b in but])
                right.Add(double,1)
            else:
                right.Add(but,1,flag=wx.EXPAND)
        self.divider.Add(left,1,flag=wx.EXPAND)
        self.divider.Add(right,0,flag=wx.EXPAND)
        self.SetSizerAndFit(self.divider)
        


# UI Test Code!
if __name__ == "__main__":
    app = wx.App(0)
    main = MainForm(None, -1, "입출금내역 작성기")
    # a = DataForm(None, 'add')
    # a.Show()
    app.MainLoop()
    