#!/usr/bin/env python

"""
Very simple test app to see if wx.XOR and/or wx.INVERT work
"""

import wx
import sys
print sys.version
print wx.__version__


class DemoFrame(wx.Frame):

    """ This window displays a button """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self,Event):
        dc = wx.PaintDC(self)

        dc.SetBackground(wx.BLUE_BRUSH)
        dc.Clear()
        dc.SetPen(wx.Pen('WHITE', 4, wx.SHORT_DASH))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawLine( 0, 100, 400, 100)
        dc.SetLogicalFunction(wx.INVERT)
        dc.DrawLine( 0, 200, 400, 200)
        dc.SetLogicalFunction(wx.XOR)
        dc.DrawLine( 0, 300, 400, 300)


if __name__ == "__main__":
    app = wx.App(False)
    frame = DemoFrame(None, size=(400, 400))
    frame.Show()
    app.MainLoop()
