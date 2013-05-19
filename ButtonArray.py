#!/usr/bin/env python

import wx

class ButtonArrayPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        Sizer =  wx.GridSizer(16, 2, 0, 0)
        
        for i in range(32):
            B = wx.Button(self, label = "button %i"%i)
            B.Bind(wx.EVT_BUTTON,
                   lambda evt, but_num = i: self.OnButton(evt, but_num) )
            Sizer.Add(B, 0, wx.GROW|wx.ALL, 4)
        
        self.SetSizerAndFit(Sizer)
                   
    def OnButton(self, evt, but_num):
        print "Button number: %i clicked"%but_num
        
            
    

class DemoFrame(wx.Frame):

    def __init__(self, title = "Button Array Demo"):
        wx.Frame.__init__(self, None , -1, title)


        btn = wx.Button(self, label = "Quit")
        btn.Bind(wx.EVT_BUTTON, self.OnQuit )

        BP = ButtonArrayPanel(self)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(btn, 1, wx.CENTER|wx.ALL, 6)
        Sizer.Add(BP, 0, wx.CENTER|wx.ALL, 4)
        self.SetSizerAndFit(Sizer)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        
    def OnQuit(self,Event):
        self.Destroy()
        

app = wx.App(False)
frame = DemoFrame()
frame.Show()
app.MainLoop()





