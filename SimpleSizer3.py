#!/usr/bin/env python2.3

import wx

class TestFrame(wx.Frame):
    def __init__(self, parent, ID, title = ""):
        wx.Frame.__init__(self, parent, -1, title, style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        ID_CODE = wx.NewId()

        # Set Controls
        label_name = wx.StaticText(self, -1, "Name: ")
        self.name = wx.TextCtrl(self, -1, "A name", wx.DefaultPosition, (200,20))
        label_sysfile = wx.StaticText(self, -1, "System file: ")
        self.sysfile = wx.TextCtrl(self, -1, " A file", wx.DefaultPosition, (200,20))
        button_sysfile = wx.Button(self, ID_CODE, "View Code")
        label_sysname = wx.StaticText(self, -1, "System name: ")
        self.sysname = wx.TextCtrl(self, -1, " A sysname", wx.DefaultPosition, (200,20))
        line = wx.StaticLine(self, -1)
        buttonOK = wx.Button(self, wx.ID_OK, "OK")
        buttonOK.SetDefault()
        buttonCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        # Do Layout
        sizer = wx.BoxSizer(wx.VERTICAL)


        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(label_name, 0, wx.LEFT, 5)
        box1.Add((1,1), 1)
        box1.Add(self.name, 0, wx.ALIGN_RIGHT, 5)
        sizer.Add(box1, 0, wx.EXPAND|wx.ALL, 5)

        box5 = wx.BoxSizer(wx.HORIZONTAL)
        box5.Add(label_sysfile, 0, wx.LEFT, 5)
        box5.Add((1,1), 1)
        box5.Add(self.sysfile, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER, 5)
        sizer.Add(box5, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button_sysfile, 0, wx.ALIGN_TOP|wx.ALIGN_RIGHT, 5)
        sizer.Add((1,10), 0, wx.EXPAND)

        box6 = wx.BoxSizer(wx.HORIZONTAL)
        box6.Add(label_sysname, 0, wx.LEFT, 5)
        box6.Add((1,1), 1, wx.GROW)
        box6.Add(self.sysname, 0, wx.ALIGN_RIGHT, 5)
        sizer.Add(box6, 0, wx.EXPAND|wx.ALL, 5)

        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        sizer.Add((1,1), 1, wx.EXPAND)

        box7 = wx.BoxSizer(wx.HORIZONTAL)
        box7.Add(buttonOK, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        box7.Add(buttonCancel, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add(box7, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        
    def OnCloseWindow(self, event):
        self.Destroy()

class App(wx.App):
    def OnInit(self):
        frame = TestFrame(None, -1, "Sizer Test")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = App(0)
    app.MainLoop()
     











