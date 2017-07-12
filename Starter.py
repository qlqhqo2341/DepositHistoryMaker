#-*- coding:utf-8 -*-
import wx

class Form(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.referrers = ['friends', 'advertising', 'websearch', 'yellowpages']
        self.colors = ['blue','red','yellow','orange','green','purple',
            'navy blue','black','gray']
        self.createControls()
        self.bindEvents()
        self.doLayout()
    def createControls(self):
        self.logger = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.saveButton = wx.Button(self, label="Save")
        self.nameLabel = wx.StaticText(self, label="Your name : ")
        self.nameTextCtrl = wx.TextCtrl(self, value="Enter here your name")
        self.referrerLabel = wx.StaticText(self, label="How did you hear from us?")
        self.referrerComboBox = wx.ComboBox(self, choices=self.referrers,
            style=wx.CB_DROPDOWN)
        self.insuranceCheckBox = wx.CheckBox(self,
            label="Do you wnat Insured Shipment?")
        self.colorRadioBox = wx.RadioBox(self,
            label="What color woud you like?",
            choices=self.colors, majorDimension=3, style=wx.RA_SPECIFY_COLS)
    def bindEvents(self):
        for control, event, handler in \
            [(self.saveButton, wx.EVT_BUTTON, self.onSave),
             (self.nameTextCtrl, wx.EVT_TEXT, self.onNameEntered),
             (self.nameTextCtrl, wx.EVT_CHAR, self.onNameChanged),
             (self.referrerComboBox, wx.EVT_COMBOBOX, self.onReferrerEntered),
             (self.referrerComboBox, wx.EVT_TEXT, self.onReferrerEntered),
             (self.insuranceCheckBox, wx.EVT_CHECKBOX, self.onInsuranceChanged),
             (self.colorRadioBox, wx.EVT_RADIOBOX, self.onColorChanged)]:
            control.Bind(event, handler)
    def doLayout(self):
        '''Need To ReDefine'''
        raise NotImplementedError
    
    #CallBack methods
    
    def onColorChanged(self, event):
        self.__log('User wants color: %s'%(self.colors[event.GetInt()]))
    
    def onReferrerEntered(self, event):
        self.__log('User entered referrer: %s'%(event.GetString()))
    
    def onSave(self, event):
        self.__log('User clicked on button with id %d'%(event.GetId()))
    
    def onNameEntered(self, event):
        self.__log('User entered Name: %s'%(event.GetString()))
    
    def onNameChanged(self, event):
        self.__log('User typed Character: %d'%event.GetKeyCode())
        event.Skip()
    
    def onInsuranceChanged(self, event):
        self.__log('User wants insurance: %s'%(bool(event.IsChecked())))

    #Helper Methods

    def __log(self, message):
        '''private method to append aa string to the logger text control.'''
        self.logger.AppendText('%s\n'%message)

class FormWithAbsolutePositioning(Form):
    def doLayout(self):
        for control, x, y, width, height in \
            [(self.logger, 300, 20, 200, 300),
             (self.nameLabel, 20, 60, -1, -1),
             (self.nameTextCtrl, 150, 60, 150, -1),
             (self.referrerLabel, 20, 90, -1, -1),
             (self.referrerComboBox, 150, 90, 95, -1),
             (self.insuranceCheckBox, 20, 180, -1, -1),
             (self.colorRadioBox, 20, 210, -1, -1),
             (self.saveButton, 200, 300, -1, -1)]:
            control.SetDimensions(x=x,y=y,width=width,height=height)

class FormWithSizer(Form):
    def doLayout(self):
        boxSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        gridSizer = wx.FlexGridSizer(rows=5, cols=2, vgap=10, hgap=10)

        expandOption = dict(flag=wx.EXPAND)
        noOption = dict()
        emptySpace = ((0,0), noOption)

        for control, option in \
            [(self.nameLabel, noOption),
             (self.nameTextCtrl, expandOption),
             (self.referrerLabel, noOption),
             (self.referrerComboBox, expandOption),
             emptySpace,
             (self.insuranceCheckBox, noOption),
             emptySpace,
             (self.colorRadioBox, noOption),
             emptySpace,
             (self.saveButton, dict(flag=wx.ALIGN_CENTER))]:
            gridSizer.Add(control, **option)

        for control, options in \
            [(gridSizer, dict(border=5, flag=wx.ALL)),
             (self.logger, dict(border=5, flag=wx.ALL|wx.EXPAND, proportion=1))]:
            boxSizer.Add(control, **options)
        self.SetSizerAndFit(boxSizer)

class FrameWithForms(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(FrameWithForms, self).__init__(*args, **kwargs)
        notebook = wx.Notebook(self)
        form1 = FormWithAbsolutePositioning(notebook)
        form2 = FormWithSizer(notebook)
        notebook.AddPage(form1, 'Absolute Positioning')
        notebook.AddPage(form2, 'Sizers')
        self.SetClientSize(notebook.GetBestSize())

if __name__ == '__main__':
    app = wx.App(0)
    frame = FrameWithForms(None, title='Demo with Notebook')
    frame.Show()
    app.MainLoop()