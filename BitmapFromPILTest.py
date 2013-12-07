#!/usr/bin/env python

"""
A test of making wx.Bitmap from a PIL image
"""

import wx
import PIL.Image

class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title = "Bitmap Demo"):
        wx.Frame.__init__(self, None , -1, title)#, size = (800,600), style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        # load the PIL image:

        image = PIL.Image.open('splash.png')
        image = image.convert('RGB')
        image = image.resize((100,100), PIL.Image.ANTIALIAS)
        w, h = image.size
        self.bitmap = wx.BitmapFromBuffer(w, h, image.tostring() )

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 10, 10 )

    def OnQuit(self,Event):
        self.Destroy()

app = wx.App(False)
frame = DemoFrame()
frame.Show()
app.MainLoop()
