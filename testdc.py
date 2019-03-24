#!/usr/bin/env python
"""

A very simple app for testing DC functionality

"""


import wx


class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Test", wx.DefaultPosition, size=(200, 200),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        wx.EVT_PAINT(self, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        #dc.SetMapMode(wx.MM_TWIPS)
        dc.BeginDrawing()
        print("PPI :", dc.GetPPI())
        # dc.SetPPI((100,100))
        #print "PPI :", dc.GetPPI()
        for i in [("MM_TWIPS",   wx.MM_TWIPS),
                  ("MM_POINTS",  wx.MM_POINTS),
                  ("MM_METRIC",  wx.MM_METRIC),
                  ## ("MM_LOMETRIC",wx.MM_LOMETRIC),
                  ("MM_TEXT",    wx.MM_TEXT)]:
            print(i)

        print("Map Mode is:", dc.GetMapMode())

        #dc.SetBackground( wx.Brush("Blue") )
        dc.Clear()

        dc.DrawText("Text", 50, 50 )
        dc.DrawText("", 100, 50 )

        dc.DrawRotatedText("Text", 100, 100, 90)
        dc.DrawRotatedText("more text", 100, 50, 90)

        dc.EndDrawing()


class DemoApp(wx.App):
    def OnInit(self):
        frame = TestFrame()
        frame.Show(True)

        return True


if __name__ == "__main__":
    app = DemoApp(False)
    app.MainLoop()
