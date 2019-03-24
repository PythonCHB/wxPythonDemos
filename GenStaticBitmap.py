#!/usr/bin/env python
import wx

import wx.lib.statbmp


class cWindowBitmap(wx.lib.statbmp.GenStaticBitmap):

    """
    A subclass of GenStaticBitmap, that adds some functionality
    """
    def __init__(self, parent, bitmapfilename, ImageNumber, **kwargs):

        self.bitmap = wx.Bitmap(bitmapfilename)
        wx.lib.statbmp.GenStaticBitmap.__init__(self, parent, wx.ID_ANY, self.bitmap, **kwargs)

        self.parent = parent
        self.filename = bitmapfilename
        self.ImageNumber = ImageNumber

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

    def OnLeftDown(self, event):
        print("In Left Down of:", self.filename)
        self.parent.OnBitmapClicked(self.ImageNumber)

    def OnLeftUp(self, event):
        print("In Left Up of:", self.filename)


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        # These represent "many" bitmaps.
        [Sizer.Add(cWindowBitmap(self, "Images/smalltest.jpg", i), 0, wx.ALL, 10)
            for i in range(3)]

        self.SetSizerAndFit(Sizer)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnBitmapClicked(self, ImageNumber):
        print("Image: %i was clicked" %ImageNumber)

    def OnCloseWindow(self, event):
        self.Destroy()


class App(wx.App):
    def OnInit(self):
        frame = MainFrame(None, -1, "wxWindowBitmap Test", wx.DefaultPosition, (550, 600))
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


if __name__ == '__main__':
    app = App(0)
    app.MainLoop()
