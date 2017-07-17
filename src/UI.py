import wx
import store
import printer

class StartForm(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(StartForm, self).__init__(*args, **kwargs)
        self.createControl()
        self.bindEvents()
        self.doLayout()

    def createControl(self):
        raise NotImplementedError

    def bindEvents(self):
        raise NotImplementedError

    def doLayout(self):
        raise NotImplementedError

class EditForm(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.createControl()
        self.bindEvents()
        self.doLayout()

    def createControl(self):
        raise NotImplementedError

    def bindEvents(self):
        raise NotImplementedError

    def doLayout(self):
        raise NotImplementedError


if __name__ == '__main__':
    app = wx.App(0)
    