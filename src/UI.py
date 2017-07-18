# -*- coding:utf-8 -*-
import wx
import store
import printer

class StartForm(wx.Frame):
    def __init__(self, main, *args, **kwargs):
        super(StartForm, self).__init__(*args, **kwargs)
        self.main = main
        self.createControl()
        self.bindEvents()
        self.doLayout()

    def createControl(self):
        self.NewFileButton = wx.button(self, value='새 파일')
        self.LoadButton = wx.button(self, value='불러오기')

    def bindEvents(self):
        self.NewFileButton.Bind(wx.EVT_BUTTON, self.newFile)

    def newFile(self):
        self.main.NewFile()
        self.main.Show()
        self.Hide()

    def load(self):
        store.dialogLoad()
        self.main.Show()
        self.Hide()

    def doLayout(self):
        raise NotImplementedError

class MainForm(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        self.firstForm = StartForm(self,None,-1,args[2])
        self.createControl()
        self.bindEvents()
        self.doLayout()
        self.firstForm.Show()

    def NewFile(self, path=None):
        if

    def createControl(self):
        raise NotImplementedError

    def bindEvents(self):
        raise NotImplementedError

    def doLayout(self):
        raise NotImplementedError


# UI Test Code!
if __name__ == "__main__":
    app = wx.App(0)
    main = MainForm(None, -1, "Hi!")
    app.MainLoop()
    