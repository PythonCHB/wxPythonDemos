#!/usr/bin/env python

"""
Simple app that demonstrates how to use a wx.StaticBitmap, specifically
replacing bitmap dynamically.

Note: there needs to be an "Images" directory with one or more jpegs in it in the
      current working directory for this to work

Test most recently on OS-X wxPython 2.9.3.1

But it been reported to work on lots of other platforms/versions

"""
import wx, os
print "running wx version:", wx.__version__

class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        # there needs to be an "Images" directory with one or more jpegs in it in the
        # current working directory for this to work
        self.jpgs = GetJpgList("./Images") # get all the jpegs in the Images directory
        self.CurrentJpg = 0

        self.MaxImageSize = 200
        
        b = wx.Button(self, -1, "Display next")
        b.Bind(wx.EVT_BUTTON, self.DisplayNext)

        # starting with an EmptyBitmap, the real one will get put there
        # by the call to .DisplayNext()
        self.Image = wx.StaticBitmap(self, bitmap=wx.EmptyBitmap(self.MaxImageSize, self.MaxImageSize))

        self.DisplayNext()

        # Using a Sizer to handle the layout: I never  use absolute positioning
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(b, 0, wx.CENTER | wx.ALL,10)

        # adding stretchable space before and after centers the image.
        box.Add((1,1),1)
        box.Add(self.Image, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ADJUST_MINSIZE, 10)
        box.Add((1,1),1)

        self.SetSizerAndFit(box)
        
        wx.EVT_CLOSE(self, self.OnCloseWindow)

    def DisplayNext(self, event=None):
        # load the image
        Img = wx.Image(self.jpgs[self.CurrentJpg], wx.BITMAP_TYPE_JPEG)

        # scale the image, preserving the aspect ratio
        W = Img.GetWidth()
        H = Img.GetHeight()
        if W > H:
            NewW = self.MaxImageSize
            NewH = self.MaxImageSize * H / W
        else:
            NewH = self.MaxImageSize
            NewW = self.MaxImageSize * W / H
        Img = Img.Scale(NewW,NewH)
 
        # convert it to a wx.Bitmap, and put it on the wx.StaticBitmap
        self.Image.SetBitmap(wx.BitmapFromImage(Img))

        # You can fit the frame to the image, if you want.
        #self.Fit()
        #self.Layout()
        self.Refresh()

        self.CurrentJpg += 1
        if self.CurrentJpg > len(self.jpgs) -1:
            self.CurrentJpg = 0

    def OnCloseWindow(self, event):
        self.Destroy()


def GetJpgList(dir):
    jpgs = [f for f in os.listdir(dir) if f[-4:] == ".jpg"]
    # print "JPGS are:", jpgs
    return [os.path.join(dir, f) for f in jpgs]

class App(wx.App):
    def OnInit(self):

        frame = TestFrame(None, -1, "wxBitmap Test", wx.DefaultPosition,(550,200))
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = App(0)
    app.MainLoop()
     











