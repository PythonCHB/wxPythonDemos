#!/usr/bin/env python

import wx
import time

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "DrawLines Test",
                         wx.DefaultPosition,
                         size=(500,500),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        ## Set up the MenuBar
        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()

        ID_CLEAR_MENU = wx.NewId()
        file_menu.Append(ID_CLEAR_MENU, "&Clear", "Clear the Screen")
        self.Bind(wx.EVT_MENU, self.Clear, id=ID_CLEAR_MENU)

        ID_ANIMATE_MENU = wx.NewId()
        file_menu.Append(ID_ANIMATE_MENU, "&Animate", "Animate the Screen")
        self.Bind(wx.EVT_MENU, self.Animate, id=ID_ANIMATE_MENU)

        file_menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)

        MenuBar.Append(file_menu, "&File")
        self.SetMenuBar(MenuBar)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        self.LineData = []

    def OnPaint(self,event):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("Purple"))
        dc.Clear()
        dc.SetPen(wx.Pen("Red", 3))
        for Line in self.LineData:
            dc.DrawLines(Line)

    def Clear(self, event = None):
        self.LineData = []
        self.Refresh()

    def OnLeftDown(self,event):
        xy = event.GetPosition()
        self.LineData.append([xy])

    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            xy = event.GetPosition()
            self.LineData[-1].append(xy)
            # note: Update() doesn't work
            self.Refresh()

    def Animate(self, event):
        self.Refresh()
        self.LineData.append( [] )
        for i in xrange(0,500,5):
            self.LineData[-1].append((i,i))
            self.Refresh()
            self.Update()
            time.sleep(0.01)

    def OnQuit(self,event):
        self.Close(True)


class DemoApp(wx.App):
    def OnInit(self):
        frame = TestFrame()
        frame.Show(True)
        self.SetTopWindow(frame)

        return True


if __name__ == "__main__":
    app = DemoApp(0)
    app.MainLoop()
