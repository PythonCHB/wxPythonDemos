#!/usr/bin/env pythonw

"""
Timing test of the DrawLineList DC methods

It is NOT fast!
"""

import time
import wx
from numpy import random

NumLinePoints = 500
NumPointPoints = 500

# Make some random data to draw things with.

MaxX = 500
LinesPoints = random.randint(1, MaxX, (NumLinePoints, 2))
PointsPoints = random.randint(1, MaxX, (NumPointPoints, 2))


class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
            "DrawLines Test",
            wx.DefaultPosition,
            size=(MaxX, MaxX),
            style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        # Set up the MenuBar.
        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        item = file_menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        MenuBar.Append(file_menu, "&File")

        draw_menu = wx.Menu()
        item = draw_menu.Append(wx.ID_ANY, "&ReDraw", "DrawAgain")
        self.Bind(wx.EVT_MENU, self.ReDraw, item)
        MenuBar.Append(draw_menu, "&Draw")

        self.SetMenuBar(MenuBar)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        print("in OnPaint...")
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("White"))
        dc.Clear()
        self.DrawLines(dc)
        self.DrawPoints(dc)

    def ReDraw(self, event=None):
        dc = wx.ClientDC(self)
        dc.SetBackground(wx.Brush("White"))
        dc.Clear()
        self.DrawLines(dc)
        self.DrawPoints(dc)

    def DrawLines(self, dc):
        dc.SetPen(wx.Pen('Black', 2))
        start = time.time()
        dc.DrawLines(LinesPoints)
        print("DrawLines Call took %f seconds" % (time.time() - start))
        start = time.time()
        for i in range(len(LinesPoints) - 1):
            dc.DrawLine(
                LinesPoints[i, 0],
                LinesPoints[i, 1],
                LinesPoints[i + 1, 0],
                LinesPoints[i + 1, 1],
            )
        print("DrawLine loop took %f seconds" % (time.time() - start))

    def DrawPoints(self, dc):
        dc.SetPen(wx.Pen('Red', 2))
        start = time.time()
        dc.DrawPointList(PointsPoints)
        print("DrawPointList Call took %f seconds" % (time.time() - start))

    def OnQuit(self, event):
        self.Close(True)


class DemoApp(wx.App):
    def OnInit(self):
        frame = TestFrame()
        frame.Show(True)
        self.SetTopWindow(frame)

        return True


if __name__ == "__main__":
    app = DemoApp(False)
    app.MainLoop()
