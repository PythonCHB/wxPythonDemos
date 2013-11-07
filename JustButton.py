#!/usr/bin/env python

import wx
import wx.lib.buttons

class ButtonPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        btn = wx.Button(self, label = "Push Me", pos=(40,60), size=(120,-1))
        btn = wx.Button(self, label = "Push Me Also", pos=(80,30), size=(200, 60))
        btn = wx.Button(self, label = "No, push me!", pos=(90,110), size=(65, 80))
        btn = wx.lib.buttons.GenButton(self, label = "better?", pos=(40,150), size=(60, 60))

        btn.Bind(wx.EVT_BUTTON, self.OnButton )

    def OnButton(self, evt):
        print "Button Clicked"


class DemoFrame(wx.Frame):
    """ This frame displays a panel with a button] """
    def __init__(self, title = "Micro App"):
        wx.Frame.__init__(self, None , -1, title)

        pnl = ButtonPanel(self)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        
    def OnQuit(self,Event):
        self.Destroy()
        

app = wx.App(False)
frame = DemoFrame()
frame.Show()
app.MainLoop()





