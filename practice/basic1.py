import wx

class MainForm(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        self.createControls()
        self.bindEvents()
        self.doLayout()
        
    def createControls(self):
        self.text = wx.TextCtrl(self, value="Please Input Data")
        self.val = wx.StaticText(self, label="init")
    
    def bindEvents(self):
        self.text.Bind(wx.EVT_TEXT_ENTER, self.Entered)
    
    def doLayout(self):
        self.sizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizer.Add(self.text, border=5, flag=wx.ALL)
        self.sizer.Add(self.val, border=5, flag=wx.ALL)
        self.SetSizerAndFit(self.sizer)

    #Event Method
    def Entered(self, evt):
        self.val.SetLabelText(evt.GetString())


if __name__ == "__main__":
    app = wx.App(0)
    frame = MainForm(None, -1, "Hello")
    frame.Show()
    app.MainLoop()