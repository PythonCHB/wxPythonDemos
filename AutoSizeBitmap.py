#!/usr/bin/env python

"""
AutoSizeBitmap.py

Example for how to have a bitmap autosize itself in wxPython
"""
import math
import wx

KEEP_ASPECT_RATIO = True


class AutoSizeFrame(wx.Frame):
    def __init__(self, image, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.aspect_ratio = float(image.Width) / float(image.Height)
        self.canvas = AutoSizeBitmap(image, self)
        self.canvas.SetSize((300, 400))

        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Fit()
        self.Show()

    def OnSize(self, evt=None):
        size = self.Size
        if (size[0] > 0 and size[1] > 0):
            width, height = size
            if KEEP_ASPECT_RATIO:
                total_size = width * height
                height = int(math.sqrt(total_size / self.aspect_ratio))
                width = int(total_size / height)
                # resize window on the fly to keep the aspect ratio
                self.SetSize((width, height))
            self.canvas.SetSize((width, height))


class AutoSizeBitmap(wx.Window):
    """
    A subclass of wx.Window that will hold an image (much like a StaticBitmap),
    but re-size it to fit the current size of the Window
   """
    def __init__(self, image, *args, **kwargs):
        """
        initialize an AutoSizeBitmap

        :param parent: parent Window for this window
        :param image: a wx.Image that you want to display
        """
        wx.Window.__init__(self, *args, **kwargs)

        self.orig_image = image
        self.bitmap = None
        self.prev_size = self.Size

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnSize(self, evt=None):
        size = self.Size
        if size[0] > 0 and size[1] > 0:
            img = self.orig_image.Copy()
            img.Rescale(*size)
            self.bitmap = wx.BitmapFromImage(img)
            self.Refresh()

    def OnPaint(self, evt=None):
        dc = wx.PaintDC(self)
        try:
            dc.DrawBitmap(self.bitmap, 0, 0)
        except ValueError:  # in case bitmap has not yet been initialized
            pass

if __name__ == "__main__":
    import sys

    try:
        filename = sys.argv[1]
    except:
        filename = "Images/cute_close_up.jpg"
    App = wx.App(False)
    img = wx.Image(filename)
    f = AutoSizeFrame(img, None, size=(400, 600))
    App.MainLoop()

