# -*- coding:utf-8 -*-
import wx
import re
import sys

dhData, file_path = {}, None
is_tracing, is_saved = False, True
activityData , undoCount, history_size = [], 0, 6
mainForm = None

def init(Frame):
    global dhData, file_path, is_tracing, is_saved
    global activityData, undoCount, history_size
    global mainForm
    dhData, file_path = {}, None
    is_tracing, is_saved = True, True
    activityData , undoCount, history_size = [], 0, 6
    mainForm = Frame
    mainForm.refresh()

def typeChecking(items,flag=None):
    if not isinstance(items, list):
        print >>sys.stderr,"typechecking receive not list as argument"
        return
    passList = set(range(len(items)))
    checkList = [
        re.compile(r'\d{4}-\d{1,2}-\d{1,2}'), # date
        re.compile(r'[^,]?'), # fest
        re.compile(r'[^,]+'), # body
        re.compile(r'-?\d') # value
    ]
    # if userdata, value checks twice
    checkList += [checkList[-1]] if flag=='userdata' else [] 
    for ind,item in enumerate(items):
        for checker,obj in zip(checkList,item):
            if not checker.match(obj):
                passList.discard(ind)
    return passList

def tracingOn():
    '''
    If tracing on (use add or modify) after undo
    Need to remove activityData behind undoCount data
    '''
    global undoCount
    for i in range(undoCount):
        activityData.pop(-1)
    undoCount=0
    is_tracing = True

def acitivityWriter(func):
    if is_tracing:
        def callf(*args): # Only add, del, modify. Don't need to **kwargs
            if len(activityData) == history_size:
                activityData.pop(0)
            
            activityData.append((func,args))
            r = func(*args)
            return r
        return callf
    else:
        return func

@acitivityWriter
def add(obj):
    # TODO : check the text is not have comma (,)
    if not isinstance(obj,list):
        print >>sys.stderr,"AddFunc receive not list as argument"
        return
    
    

    
@acitivityWriter
def remove(obj):
    '''This Function is Temporary used for presenting selected rows'''
    box = wx.MessageBox(str(obj))
    box.ShowModal()


@acitivityWriter
def modify(prev, next):
    pass
    

def dialogNotSaving():# call dialog for closing after not saved
    dialog = wx.MessageDialog(mainForm, 'hohoh', style=wx.YES_NO|wx.CANCEL)
    r = dialog.ShowModal()
    return r

def dialogSave(evt=None): # call dialog and saving
    dialog = wx.FileDialog(None, "Save File", "","","DH Files (*.dh)|*.dh",
     wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    if dialog.ShowModal() == wx.ID_CANCEL:
        return
    
    mainForm.SetTitle("File : "+dialog.GetPath())
    save(dialog.GetPath())

def dialogLoad(evt=None): # call dialog and loading
    dialog = wx.FileDialog(None, "Open FIle","","","DH Files (*.dh)|*.dh",
     wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

    if dialog.ShowModal() == wx.ID_CANCEL:
        return

    mainForm.SetTitle(u"입출금내역작성기"+" File : "+dialog.GetPath())
    load(dialog.GetPath())

def save(path):
    is_saved = True
    with open(path, 'wt') as f:
        for ref in dhData:
            val = dhData[ref]
            str = "%s, %s, %s, %d"%(ref[0],ref[1],ref[2],int(val))
            print >>f,str
                                   
    
def load(path):
    init(mainForm)
    with open(path) as f:
        for str in f:
            r = [t.strip() for t in str.split(',')]
            date, fest, body, val = r
            
            # TODO: need to check right type
            dhData[date, fest, body]=int(val)      
    mainForm.refresh()

def supportSequence(ori_func):
    def core(args):
        if isinstance(args,list) or isinstance(args,tuple):
            r = [core(i) for i in args]
            return r
        else:
            return ori_func(args)
    return core

@supportSequence
def moneyStr(obj):
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

@supportSequence
def unMoneyStr(obj):
    return obj.replace(',','')