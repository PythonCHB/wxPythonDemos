#!/usr/bin/env python2.3

import wx

class TestFrame(wx.Frame):
    def __init__(self,parent, id,title,position,size):

        wx.Frame.__init__(self, parent, -1, title, style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.panel1 = wx.Panel(self, -1, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER)
        self.exit = wx.Button(self, -1, "Exit")
        wx.EVT_BUTTON(self, self.exit.GetId(), self.OnCloseWindow)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.panel1,1, wx.EXPAND|wx.ALL,10)
        box.Add(self.exit,0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 4)
        self.SetSizer(box)

        wx.EVT_CLOSE(self, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()

class App(wx.App):
    def OnInit(self):
        frame = TestFrame(wx.NULL, -1, "Sizer Test", wx.DefaultPosition,(400,400))
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = App(0)
    app.MainLoop()
     











