#!/usr/bin/env python

# I Always specify the python version in the #! line, it makes it much
# easier to have multiple versions on your system

import wx


class ColoredPanel(wx.Panel):
    def __init__(self, parent, color):
        wx.Panel.__init__(self, parent, -1, style=wx.SIMPLE_BORDER)
        self.SetBackgroundColour(color)

        self.exit = wx.Button(self, -1, "Exit")
        wx.EVT_BUTTON(self, self.exit.GetId(), self.OnExit)

        # maybe it's not worth a sizer for one control, but it does make it easy to put a border around it, etc.
        # and here it is if you want to add more controls.

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.exit, 0, wx.ALL, 4)

        self.SetSizer(box)
        self.Fit()

    def OnExit(self, event):
        # Note: this is an ugly way to do this...
        self.GetParent().OnCloseWindow(None)


class TestFrame(wx.Frame):
    def __init__(self, parent, id, title, position, size):

        wx.Frame.__init__(self, parent, -1, title, style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.panel1 = wx.Panel(self, -1, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER)
        self.panel2 = ColoredPanel(self, wx.RED)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.panel1, 1, wx.EXPAND | wx.ALL)
        box.Add(self.panel2, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT)
        self.SetSizer(box)

        self.Show(1)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()


class App(wx.App):
    def OnInit(self):
        frame = TestFrame(None, -1, "Sizer Test", wx.DefaultPosition, (400, 400))
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


if __name__ == "__main__":
    app = App(0)
    app.MainLoop()
