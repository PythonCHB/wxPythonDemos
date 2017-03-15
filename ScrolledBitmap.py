#!/usr/bin/env

import wx

# set an image file here
img_filename = 'Images/white_tank.jpg'


class MyCanvas(wx.ScrolledWindow):
    def __init__(self, *args, **kwargs):
        wx.ScrolledWindow.__init__(self, *args, **kwargs)

        self.bmp = wx.Image(img_filename).ConvertToBitmap()

        self.maxWidth, self.maxHeight = self.bmp.GetWidth(), self.bmp.GetHeight()

        self.SetScrollbars(20, 20, self.maxWidth / 20, self.maxHeight / 20)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        # an arbitrary rect to draw -- in pixel coords
        self.rect = (200, 200, 300, 200)  # x, y, width, height

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)

        dc.SetPen(wx.Pen(wx.RED, 2))
        dc.SetBrush(wx.Brush((255, 255, 255, 85)))

        dc.DrawBitmap(self.bmp, 0, 0)
        dc.DrawRectangle(*self.rect)


class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        wx.EVT_CLOSE(self, self.OnCloseWindow)

        self.Canvas1 = MyCanvas(self, wx.NewId())

    def OnCloseWindow(self, event):
        self.Destroy()


class App(wx.App):
    def OnInit(self):
        frame = TestFrame(None, title="Scroll Test", size=(800, 700))
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == "__main__":

    app = App(False)

    app.MainLoop()












