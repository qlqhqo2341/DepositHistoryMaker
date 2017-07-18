from UI import MainForm
import wx

dhData = {}
activityData = []
undoCount=0
is_tracing = False
history_size = 6
file_path = None

def tracingOn():
    '''
    If tracing on (use add or modify) after undo
    Need to remove activityData behind undoCount data
    '''
    if undoCount > 0:
        # TODO : make function!
        pass
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
    pass

@acitivityWriter
def remove(obj):
    pass

@acitivityWriter
def modify(prev, next):
    pass
    

def dialogSave(): # call dialog and saving
    pass
def dialogLoad(): # call dialog and loading
    pass

def save(path):
    with open(path, 'wt') as f:
        for ref in dhData:
            val = dhData[ref]
            str = "%s, %s, %s, %d"%(ref[0],ref[1],ref[2],int(val))
            print >>f,str
                                   
    
def load(path):
    with open(path) as f:
        for str in f:
            r = [t.strip() for t in str.split(',')]

        # TODO: need to check right type
        dhData[(r[0],r[1],r[2])]=int(r[3])      

if __name__ == '__main__':
    app = wx.App(0)
    frame = MainForm(None, -1, "Edit : ")
    frame.start(0)
    app.MainLoop()