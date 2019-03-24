#!/usr/bin/env python

import wx


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__ (self, parent, id, title, size = (300, 300))

        globalSizer=wx.BoxSizer(wx.VERTICAL)

        title=wx.StaticText(self, -1, "Title")
        nameText = wx.StaticText(self, -1, "Name")

        self.NameTextCtrl = wx.TextCtrl(self,wx.NewId(), "", size=(500, 25))

        self.ListCtrl = wx.ListCtrl(self, wx.NewId())

        globalSizer.Add(title , 0, wx.ALIGN_LEFT | wx.BOTTOM, 5)
        globalSizer.Add(nameText, 0, wx.ALIGN_LEFT)
        globalSizer.Add(self.NameTextCtrl ,0,wx.EXPAND | wx.BOTTOM, 5)
        globalSizer.Add(self.ListCtrl, 1, wx.EXPAND)

        self.SetSizer(globalSizer)
        self.Show()


if __name__ == "__main__":
    app = wx.App(0)
    Panel = MyFrame(None, -1, "Sizer Test 3")

    app.MainLoop()
