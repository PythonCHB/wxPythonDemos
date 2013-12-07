#!/usr/bin/env python

import wx

import os
import time


class MySplashScreen(wx.SplashScreen):
    def __init__(self, imageFileName):
        bmp = wx.Bitmap(imageFileName)
        wx.SplashScreen.__init__(self, bitmap=bmp,
                                 splashStyle=wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 milliseconds=5000, parent=None)

        self.Bind(wx.EVT_CLOSE, self.OnExit)
        wx.Yield()

    def OnExit(self, event):
        """"""
        self.Hide()
        event.Skip() # Make sure the default handler runs too...
        self.ShowMain()

    def ShowMain(self):
        print "ShowMain called"
        frame = MainFrame(None, title="An Empty Frame")
        frame.CenterOnScreen()
        frame.Show()



class MainFrame(wx.Frame):
    """
    this is an empty frame, just to have something to show
    """
    pass


class App(wx.App):
    def OnInit(self):
        """
        This gets called when the App Starts up
        """

        Splash = MySplashScreen(SplashImageFile)
        frame = MainFrame(None, title="Main Frame")
        frame.Show()

        return True


if __name__ == "__main__":
    SplashImageFile = "Images/cute_close_up.jpg"
    app = App(0)
    app.MainLoop()
