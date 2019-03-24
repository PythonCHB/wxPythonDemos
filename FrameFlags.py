#!/usr/bin/env python

if __name__ == '__main__':
    import wx
    app = wx.App(False)
    def OnClose(event):
        frame.Close()
    frame = wx.Frame(None,
                     title = "Frame Style Test",
                     style=wx.DEFAULT_FRAME_STYLE & ~wx.CLOSE_BOX)
    frame.Bind(wx.EVT_RIGHT_UP, OnClose)
    frame.Show()
    app.MainLoop()
