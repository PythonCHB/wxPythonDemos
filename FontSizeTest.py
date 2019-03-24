#!/usr/bin/env python
"""
Simple demo/sample for testing Font Size with a DC --
using wx.FontFromPixel Size
"""

from __future__ import division, unicode_literals, print_function

import wx


class MyPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.Draw(dc)

    def Draw(self, dc):
        dc.Clear()
        x, y = 20, 0
        for fs in [8, 10, 12, 14, 18, 20, 30, 60]:
            y += 1.2 * fs
            w = fs * 11
            S = wx.Size((0, fs))
            # S = wx.Size((fs, fs))
            text = "%i pixel Font and Box" % fs
            Font = wx.Font(S, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=True)
            dc.SetFont(Font)
            E = dc.GetTextExtent(text)
            dc.SetFont(Font)
            E = dc.GetTextExtent(text)
            print("Font size: %s, Extent ratio: %s" % (S, E[0] / E[1]))
            print("font point size::", Font.GetPointSize())
            dc.DrawText(text, x, y)
            dc.DrawRectangle(x, y, w, fs)
            dc.DrawText(text, x, y)


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="test", size=(500, 500))

        self.Panel = MyPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.Panel, 1, wx.EXPAND)

        self.SetSizer(sizer)

if __name__ == '__main__':
    app = wx.App(0)
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
