#!/usr/bin/env python

"""
A small program to produce a "magnifying glass" effect over an image.

Adapted from code posted to wxPython-users by Peter Damoc


"""

##try:
##    import fixdc
##except ImportError:
##    pass # If you get an error like: DC_DrawBitmap() takes at most 4 arguments (5 given)
##         # you need the fixdc module, and don't have it

import wx


class MyCanvas(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.bmp = wx.Bitmap('splash.gif')
        self.mpos = (0, 0)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.SampleSize = 40
        self.ZoomedSize = 160

    def OnMouseMove(self, evt):
        self.mpos = evt.GetPosition()
        self.Refresh(False)
        evt.Skip()

    def OnPaint(self, evt):
        self.size = self.GetSize()
        x = max(self.mpos[0] - 20, 0)
        y = max(self.mpos[1] - 20, 0)
        zoomed = None
        try:
            zoomed = self.bmp.GetSubBitmap((x-self.SampleSize/2,
                                            y-self.SampleSize/2,
                                            self.SampleSize,
                                            self.SampleSize)).ConvertToImage()
            zoomed.Rescale(self.ZoomedSize, self.ZoomedSize)
            zoomed = zoomed.ConvertToBitmap()
        except wx._core.PyAssertionError:
            zoomed = None

        offscreenBMP = wx.EmptyBitmap(*self.size)
        self.offDC = wx.MemoryDC()
        self.offDC.SelectObject(offscreenBMP)
        self.offDC.Clear()
        self.offDC.BeginDrawing()
        self.offDC.DrawBitmap(self.bmp, 0, 0, True)
        if zoomed is not None:
            self.offDC.DrawBitmap(zoomed,
                                  x - self.ZoomedSize / 2,
                                  y - self.ZoomedSize / 2, True)
        self.offDC.EndDrawing()
        self.dc = wx.PaintDC(self)
        self.dc.Blit(0, 0, self.size[0], self.size[1], self.offDC, 0, 0)
        evt.Skip()


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Lupa")
        canvas = MyCanvas(self)
        self.SetSize((canvas.bmp.GetWidth(), canvas.bmp.GetHeight()))
        self.Show()


if __name__ == "__main__":
    app = wx.App(0)
    Frame()
    app.MainLoop()
