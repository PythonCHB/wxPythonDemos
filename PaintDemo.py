#!/usr/bin/python

import wx
from random import *

class MyPanel(wx.Panel):
    def __init__(self, parent, size, position):
        wx.Panel.__init__(self, parent, -1, size=size, pos=position)
        self.NewRect()

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawRectangle(*self.rect)
        
    def NewRect(self):
        self.rect = (randint(0, 300), randint(0, 300), 50, 50)

    def DrawRect(self):
        self.NewRect()
        dc = wx.ClientDC(self)
        dc.Clear()
        dc.DrawRectangle(*self.rect)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        button = wx.Button(self, -1, label="Add New")
        button.Bind(wx.EVT_BUTTON, self.UpdatePanel)

        self.Panel = MyPanel(self, (200,200), (100,250))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button,0,wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(self.Panel,1,wx.EXPAND)

        self.SetSizer(sizer)
        
    def UpdatePanel(self,event):
        self.Panel.DrawRect()

if __name__ == '__main__':
    app = wx.App(0)
    frame = MyFrame(None, title="Test", size=(500,500) )
    frame.Show()
    app.MainLoop()
    
