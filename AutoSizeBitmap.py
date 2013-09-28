#!/usr/bin/env python

"""
AutoSizeBitmap.py

Example for how to have a bitmap autosize itself in wxPython
"""

import wx

class AutoSizeBitmap(wx.Window):
    """
    A subclass of wx.Window that will hold an image (much like a StaticBitmap),
    but re-size it to fit the current size of the Window
"   """    
    def __init__(self, parent, image, *args, **kwargs):
        """
        initialize an AutoSizeBitmap
        
        :param parent: parent Window for this window
        :param image: a wx.Image that you want to display
        """
        
        wx.Window.__init__(self, parent, *args, **kwargs)

        self.orig_image = image
        self.bitmap = None
    
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnSize(self, evt=None):
        img = self.orig_image.Copy()
        img.Rescale(*self.Size)
        self.bitmap = wx.BitmapFromImage(img)
        
    def OnPaint(self, evt=None):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap,0,0)

if __name__ == "__main__":
    import sys
    
    try: 
        filename = sys.argv[1]
    except:
        filename = "Images/cute_close_up.jpg"
    App = wx.App(False)
    f = wx.Frame(None)
    img = wx.Image(filename)
    b = AutoSizeBitmap(f, img)
    f.Show()
    App.MainLoop()

