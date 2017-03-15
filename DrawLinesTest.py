#!/usr/bin/env pythonw

import wx
print wx.__version__
import numpy as np
from numpy import random
import time


NumLinePoints = 1000
NumPointPoints = 1000

## Make some random data to draw things with.
MaxX  = 500
# LinesPoints = random.randint(1, MaxX, (NumLinePoints,2) )
LinesPoints = random.randint(1, MaxX, (NumLinePoints,2) )
#PointsPoints = random_array.randint(1, MaxX, (NumPointPoints,2) )
PointsPoints = random.randint(1, MaxX, (NumPointPoints,2) ) # Numeric



class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "DrawLines Test",
                         wx.DefaultPosition,
                         size=(MaxX, MaxX),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        ## Set up the MenuBar
        MenuBar = wx.MenuBar()
        
        file_menu = wx.Menu()
        ID_EXIT_MENU = wx.NewId()
        file_menu.Append(ID_EXIT_MENU, "E&xit","Terminate the program")
        wx.EVT_MENU(self, ID_EXIT_MENU, self.OnQuit)
        MenuBar.Append(file_menu, "&File")
        
        draw_menu = wx.Menu()
        ID_DRAW_MENU = wx.NewId()
        draw_menu.Append(ID_DRAW_MENU, "&ReDraw","DrawAgain")
        wx.EVT_MENU(self, ID_DRAW_MENU,self.ReDraw)
        MenuBar.Append(draw_menu, "&Draw")

        self.SetMenuBar(MenuBar)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self,event):
        print "in OnPaint..."
        dc = wx.PaintDC(self)
        dc.SetBackground( wx.Brush("White") )
        dc.Clear()
        self.DrawLines(dc)
        self.DrawPoints(dc)

    def ReDraw(self, event = None):
        dc = wx.ClientDC(self)
        dc.SetBackground( wx.Brush("White") )
        dc.Clear()
        self.DrawLines(dc)
        self.DrawPoints(dc)

    def DrawLines(self, dc):
        dc.BeginDrawing()
        dc.SetPen(wx.Pen('Black', 2))
        start = time.clock()
        dc.DrawLines(LinesPoints)
        print "DrawLines Call took %f seconds"%(time.clock() - start)
        start = time.clock()
        for i in range(len(LinesPoints)-1):
            dc.DrawLine(LinesPoints[i,0],
                        LinesPoints[i,1],
                        LinesPoints[i+1,0],
                        LinesPoints[i+1,1],
                )
        print "DrawLine loop took %f seconds"%(time.clock() - start)
        dc.EndDrawing()

    def DrawPoints(self, dc):
        dc.BeginDrawing()
        dc.SetPen(wx.Pen('Red', 2))
        start = time.clock()
        dc.DrawPointList(PointsPoints)
        print "DrawPointList Call took %f seconds"%(time.clock() - start)
        dc.EndDrawing()

    def OnQuit(self,event):
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



















