# -*-coding:utf-8 -*-
import wx
import wx.grid as gridlib


# app = wx.App(0)
frame = wx.Frame(None, -1, 'hoho')
sizer = wx.BoxSizer()
g = gridlib.Grid(frame)
g.CreateGrid(10,10)
l = ['날짜','행사','내용','ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ']
for i in range(g.GetNumberRows()):
    for j in range(g.GetNumberCols()):
        g.SetCellValue(i,j,str((i+1)*(j+1)))
    g.SetColLabelValue(i,l[i])
g.EnableEditing(False)
g.EnableDragGridSize(False)
sizer.Add(g)
frame.SetSizerAndFit(sizer)
frame.Show()
app.MainLoop()