#!/usr/bin/env python

import wx


class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title="Micro App"):
        wx.Frame.__init__(self, None , -1, title)

        btn = wx.Button(self, label="Quit")

        btn.Bind(wx.EVT_BUTTON, self.OnQuit )

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        print("in OnPaint")
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.BLUE_BRUSH)
        dc.Clear()
        dc.SetPen(wx.RED_PEN)
        dc.DrawText('Some Text', 20, 20)
        
    def OnQuit(self,Event):
        self.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    frame = DemoFrame()
    frame.Show()
    app.MainLoop()
