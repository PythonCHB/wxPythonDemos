#!/usr/bin/env python

import wx


class MyCanvas(wx.ScrolledWindow):
    def __init__(self, parent, id):
        wx.ScrolledWindow.__init__(self, parent, id, wx.Point(0, 0), wx.DefaultSize, wx.SUNKEN_BORDER)

        self.bmp = wx.Bitmap('Images/white_tank.jpg', wx.BITMAP_TYPE_JPEG)

        self.maxWidth, self.maxHeight = self.bmp.GetWidth(), self.bmp.GetHeight()

        self.SetScrollbars(20, 20, self.maxWidth / 20, self.maxHeight / 20)

        ## parent.SetMaxSize((self.maxWidth, self.maxHeight))

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.DrawBitmap(self.bmp, 0, 0)


class TestFrame(wx.Frame):
    def __init__(self, parent, id, title, position, size):
        wx.Frame.__init__(self, parent, id, title, position, size)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.Canvas1 = MyCanvas(self, wx.NewId())

    def OnCloseWindow(self, event):
        self.Destroy()


class App(wx.App):
    def OnInit(self):
        frame = TestFrame(None, -1, "Scroll Test", wx.DefaultPosition, (550, 400))
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


if __name__ == "__main__":
    app = App(0)
    app.MainLoop()
