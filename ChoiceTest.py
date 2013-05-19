#!/usr/bin/env python2.4

import wx

class DemoFrame(wx.Frame):
    """ This window displays a wx.Choice """
    def __init__(self, title = "Micro App"):
        wx.Frame.__init__(self, None , -1, title)


        Choice = wx.Choice(self, choices = [str(x) for x in range(20)] )


        self.Fit()
        
app = wx.App()
frame = DemoFrame()
frame.Show()
app.MainLoop()





