#!/usr/bin/env python

import wx


class DemoFrame(wx.Frame):
    """ This window displays a wx.Choice """
    def __init__(self, title = "Micro App"):
        wx.Frame.__init__(self, None , -1, title)

        Choice = wx.Choice(self, choices = [str(x) for x in range(20)] )

        self.Fit()


if __name__ == "__main__":
    app = wx.App(0)
    frame = DemoFrame()
    frame.Show()
    app.MainLoop()
