#!/usr/bin/env python

import wx
import wx.stc as stc
import time

class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title="Timer Demo"):
        wx.Frame.__init__(self, None , -1, title, size=(500,400))

        self.TextCtrl = stc.StyledTextCtrl(self, wx.NewId())

        self.StartTime = time.time()
        self.Counter = 0
        self.Interval = 5 # interval in seconds
        # now set up the timer:
        self.Timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Timer.Start(500)

    def OnTimer(self,Event):
        CurTime = time.time() # (you might want to use time.clock on Windows)
        NumIntervals = int((CurTime - self.StartTime) / self.Interval)
        if NumIntervals >= self.Counter:
            TimeString = time.strftime("%c", time.localtime(CurTime))
            self.TextCtrl.AddText("Time: %s: Interval number: %i\n" %(TimeString,NumIntervals))
            self.Counter+= 1

    def OnQuit(self,Event):
        self.Destroy()


if __name__ == "__main__":
    app = wx.App(0)
    frame = DemoFrame()
    frame.Show()
    app.MainLoop()
