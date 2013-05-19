#!/usr/bin/env python

import wx

class MyPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.RED_BRUSH)
        x = 100 
        y = 100
        w = 50
        h = 50
        for angle in [0, 90, 180, 270, -90, -180, -270]:
            dc.DrawEllipticArc(x, y, w, h, 0, angle)
            dc.DrawText(`angle`, x+w+10, y+h/2)
            y+=100

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.Panel = MyPanel(self)

        #self.Fit()

if __name__ == '__main__':
    app = wx.App(0)
    frame = MyFrame(None, title="Test", size=(300, 800) )
    frame.Show()
    frame.Fit()
    app.MainLoop()
    
