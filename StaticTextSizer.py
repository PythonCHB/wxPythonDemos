#!/usr/bin/env python2.3

import wxversion
wxversion.select("2.5.3")
#wxversion.select("2.5.1")
#wxversion.select("2.4")

import wx
#print "Using version:", wx.__version__

class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title = "Micro App"):
        wx.Frame.__init__(self, None , -1, title)

        title = wx.StaticText(self, wx.NewId(), "The top title")

        self.Static = wx.StaticText(self, wx.NewId(), "default")

        text = wx.TextCtrl(self, wx.NewId())

        btn = wx.Button(self, wx.NewId(), "Resize")
        wx.EVT_BUTTON(self, btn.GetId(), self.OnChange )

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer.Add(self.Static, 0, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER, 4)
        sizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER | wx.ADJUST_MINSIZE , 4)
        self.SetSizer(sizer)

        self.sizer = sizer
        self.Fit()

        self.Labels = ["One label",
                       "Another Label",
                       "Yet Another Label",
                       "A now a really really long one",
                       "A short one",
                       "short"]
        self.Curlabel = 0
        
    def OnChange(self,Event):
        self.Curlabel += 1
        if self.Curlabel > len(self.Labels)-1:
            self.Curlabel = 0
        self.Static.SetLabel(self.Labels[self.Curlabel])
        self.sizer.SetItemMinSize(self.Static, self.Static.GetBestSize() )
        #self.sizer.Layout()
        self.Fit()

app = wx.PySimpleApp(0)
frame = DemoFrame()
frame.Show()
app.MainLoop()





