#!/usr/bin/env python2.4

# I Always specify the python version in the #! line, it makes it much
# easier to have multiple versions on your system
import wxversion
wxversion.select("2.6")
## Note: it may well work with other versions, but it's been tested on 2.6.
import wx

import os, time

class MySplashScreen(wx.SplashScreen):
    def __init__(self,imageFileName):
        bmp = wx.Bitmap(imageFileName) 
        wx.SplashScreen.__init__(self,
                                 bitmap = bmp,
                                 splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 milliseconds = 5000,
                                 parent = None)
        #self.Bind(wx.EVT_CLOSE, self.OnClose)
        #self.fc = wx.FutureCall(2000, self.ShowMain)

    def OnClose(self, evt):
        print "OnClose Called"
        # Make sure the default handler runs too so this window gets
        # destroyed
        #evt.Skip()
        #self.Hide()
        
        # if the timer is still running then go ahead and show the
        # main frame now
        #if self.fc.IsRunning():
        #    self.fc.Stop()
        self.ShowMain()


    def ShowMain(self):
        print "ShowMain called"
        frame = MainFrame(None, title="An Empty Frame")
        frame.CenterOnScreen()
        frame.Show()
        #if self.fc.IsRunning():
        #    self.Raise()

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
        frame = MainFrame(None, title = "Main Frame")
        frame.Show()
        #Splash.Show(True)
        return True

if __name__ == "__main__":
    SplashImageFile = "Images/cute_close_up.jpg"
    app = App(0)
    app.MainLoop()
     











