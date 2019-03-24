#!/usr/bin/env python

"""
ImageWindow.py

A wx component for a resazable window that holds an image

"""

import wx


class ImageWindow(wx.Window):
    """
    ImageWindow(Image, *args, **kwargs)

    Image: A wx.Image
    *args and **kwargs are passed in to wx.Window
    """

    def __init__(self, Image, *args, **kwargs):
        wx.Window.__init__(self, *args, **kwargs)

        self.Image = Image
        self._buffer = None
        self.Proportional = True
        self.BackgroundColor = "Blue"

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda evt: None)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self._buffer, 0, 0)

    def OnSize(self, event):
        w, h = self.GetSize()
        if not self.Proportional:
            # scale the image to the new window size
            Img = self.Image.Scale(w, h)
            self._buffer = wx.BitmapFromImage(Img)
        else:
            # scale the image, preserving the aspect ratio
            iw = self.Image.GetWidth()
            ih = self.Image.GetHeight()
            if float(iw) / ih > float(w) / h:
                NewW = w
                NewH = w * ih / iw
            else:
                NewH = h
                NewW = h * iw / ih
            Img = self.Image.Scale(NewW,NewH)
            # now build the buffer
            self._buffer = wx.EmptyBitmap(w, h)
            dc = wx.MemoryDC()
            dc.SelectObject(self._buffer)
            dc.SetBackground(wx.Brush(self.BackgroundColor))
            dc.Clear()
            x = (w - NewW) / 2
            y = (h - NewH) / 2
            dc.DrawBitmap(wx.BitmapFromImage(Img), x, y)
        self.Refresh(False)


if __name__ == "__main__":
    import TestImage


    class TestFrame(wx.Frame):
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, *args, **kwargs)

            # there needs to be an image here:
            Image = TestImage.getImage()

            # Using a Sizer to handle the layout: I never like to use absolute postioning
            box = wx.BoxSizer(wx.VERTICAL)
            # create the first ImageWindow
            IW = ImageWindow(Image, self)
            IW.Proportional = False
            box.Add(IW, 1, wx.ALL | wx.EXPAND, 10)
            # create the second ImageWindow
            IW = ImageWindow(Image, self)
            IW.Proportional = True
            IW.BackgroundColor = "Red"
            box.Add(IW, 1, wx.ALL | wx.EXPAND, 10)

            self.SetSizer(box)


    class App(wx.App):
        def OnInit(self):
            frame = TestFrame(None, title="ImageWindow Test", size=(300, 300))
            self.SetTopWindow(frame)
            frame.Show(True)
            return True

    app = App(False)
    app.MainLoop()
