# -*- coding:utf-8 -*-
import wx, store
import wx.grid as gridlib
from store import moneyStr,unMoneyStr

class DataForm(wx.Frame):
    def __init__(self,mainform,flag,data=None):
        self.mainform=mainform
        self.flag=flag
        self.data=data
        #Test code
        if flag=='modify' and not isinstance(data,list):
            print "Wrong input data in create DataForm"
            raise SystemExit()
               
        title = '추가' if flag=='add' else '수정'
        super(DataForm, self).__init__(None,-1,title,
            style=wx.DEFAULT_FRAME_STYLE ^ \
                wx.MAXIMIZE_BOX ^ \
                wx.RESIZE_BORDER)
        self.createControl()
        self.bindEvent()
        self.doLayout()       

    #Events
    # TODO : many things events
    # enter at last cell -> make new rows, resizing form (or make scroll)
    # if day and fest entered and next cell -> auto fill

    def onOk(self, evt):
        # TODO : use store.add and mainform.refresh() and destroy self
        rights = store.typeChecking(obj)
        finalList = [ obj[i] for i in rights ]

        store.add(finalList)
        
        pass

    def onCancel(self,evt):
        # TODO : destory self
        self.mainform.dataForm = None
        self.Destroy()
        pass

    def onCellChanging(self,evt):
        r,c = evt.GetRow(), evt.GetCol()
        totalR = self.sheet.GetNumberRows()
        getValue, setValue = self.sheet.GetCellValue, self.sheet.SetCellValue
        if c in range(3,5):
            if totalR == r+1: # if last record, add record
                self.sheet.AppendRows()
            if getValue(r,1) != '': # Fest is exist
                setValue(r+1,0,getValue(r,0)) #next copy
                setValue(r+1,1,getValue(r,1))
                self.sheet.SetGridCursor(r+1,2)
                self.sheet.MakeCellVisible(r+1,2)
            else:
                self.sheet.SetGridCursor(r+1,0)
                self.sheet.MakeCellVisible(r+1,0)
        evt.Skip()

    #Widgets
    def createControl(self):
        self.sheet = gridlib.Grid(self)
        self.sheet.CreateGrid(13 if self.flag=='add' else len(self.data), 5)

        for ind,name in enumerate(['날짜','행사','내용','수입','지출']):
            self.sheet.SetColLabelValue(ind,name)
        self.sheet.SetRowLabelSize(0)
        self.sheet.DisableDragGridSize()
        self.sheet.ShowScrollbars(True,True)
                
        size = (100,30)
        self.okButton = wx.Button(self, label='완료', size=size)
        self.cancelButton = wx.Button(self, label='취소',size=size)

    def bindEvent(self):
        self.okButton.Bind(wx.EVT_BUTTON, self.onOk)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)
        self.sheet.Bind(gridlib.EVT_GRID_CELL_CHANGING, self.onCellChanging)    

    def doLayout(self):
        box, buttons = wx.BoxSizer(), wx.BoxSizer(orient=wx.VERTICAL)
        buttons.AddMany([
            (self.okButton, 1, wx.EXPAND),
            (self.cancelButton, 1, wx.EXPAND)
        ])
        box.AddMany([(self.sheet,1,wx.EXPAND),(buttons,0,wx.EXPAND)])

        self.SetSizerAndFit(box)


# UI Test Code!

if __name__ == '__main__':
    app = wx.App(0)
    a = DataForm(None, 'add')
    a.Show()
    app.MainLoop()