#!/usr/bin/env python

import wx

app = wx.App(False)
frame = wx.Frame(None,
                 title = "Frame Style Test"
                 style=wx.DEFAULT_FRAME_STYLE & ~wx.CLOSE_BOX)
frame.Show()
app.MainLoop()





