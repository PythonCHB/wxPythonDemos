#!/usr/bin/env python

"""
Note that this doesn't work right!

I don't remember if it ever did
"""

import wx


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=wx.Size(360, 240))
        self.panel = MyPanel(self)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()


class MyPanel(wx.Panel):
    def __init__(self, window):
        wx.Panel.__init__(self, window, wx.NewId(), style=wx.CLIP_CHILDREN)
        self.b = wx.Button(self, -1, "Start Flashing", (50, 50))
        self.st = wx.StaticText(self, -1, "A Static Text", (50, 100), style=wx.BORDER_SUNKEN)

        wx.EVT_BUTTON(self,self.b.GetId(), self.OnButton)
        wx.EVT_PAINT(self, self.OnPaint)

        self.BorderColor = wx.RED

        self.timer = wx.Timer(self, 999)
        #self.timer.Start(300)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        self.Refresh()

    def OnTimer(self, event):
        if self.BorderColor == wx.RED:
            self.BorderColor = wx.BLUE
        else:
            self.BorderColor = wx.RED
        self.ResetBorder()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.DrawBorder(dc)
        event.Skip()

    def OnSize(self, event):
        dc = wx.ClientDC(self)
        self.DrawBorder(dc)

    def DrawBorder(self, dc):
        size = self.GetSize()
        dc.SetPen(wx.Pen(self.BorderColor, 4))
        dc.DrawRectangle(2, 2, size[0] - 3, size[1] - 3)

    def ResetBorder(self, Color=wx.RED):
        dc = wx.ClientDC(self)
        self.DrawBorder(dc)
        for c in self.GetChildren():
            c.Refresh()

    def OnButton(self,Event):
        print("Button Clicked")
        if self.timer.IsRunning():
            self.st.SetLabel("Stopping Timer")
            self.timer.Stop()
            self.b.SetLabel("Start Flashing")
        else:
            self.st.SetLabel("Starting timer")
            self.timer.Start(200)
            self.b.SetLabel("Stop Flashing")


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, "This is a test")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


if __name__ == "__main__":
    app = MyApp(0)  # Create an instance of the application class
    app.MainLoop()  # Tell it to start processing events
