#!/usr/bin/env python

import wx


class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title="Micro App"):
        wx.Frame.__init__(self, None , -1, title)

        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()

        item = wx.MenuItem(FileMenu, wx.ID_ANY, "&Quit")
        FileMenu.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnQuit, item)

        MenuBar.Append(FileMenu, "&File")
        self.SetMenuBar(MenuBar)

        panel = wx.Panel(self, -1)

        RB = wx.RadioBox(panel,
                         -1,
                         "Hedges",
                         wx.DefaultPosition,
                         wx.DefaultSize,
                         ["ABOUT", "AROUND", "ABOVE", "POSITIVE", "BELOW",
                          "VICINITY", "GENERALLY", "CLOSE", "NOT", "SOMEWHAT", "VERY", "EXTREMELY",
                          "SLIGHTLY", "AFTER", "BEFORE"],
                         2,
                         wx.RA_SPECIFY_COLS)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

    def OnQuit(self,Event):
        self.Destroy()


if __name__ == '__main__':
    app = wx.App(0)
    frame = DemoFrame()
    frame.Show()
    app.MainLoop()
