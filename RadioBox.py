#!/usr/bin/env python2.4

import wx

class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title = "Micro App"):
        wx.Frame.__init__(self, None , -1, title)#, size = (800,600), style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        
        item = wx.MenuItem(FileMenu, wx.ID_EXIT, "&Quit")
        FileMenu.Append(item)
        self.Bind(wx.EVT_MENU, self.OnQuit, item)

        MenuBar.Append(FileMenu, "&File")
        self.SetMenuBar(MenuBar)


        RB = wx.RadioBox(self,
                         label="Hedges",
                         choices = ["ABOUT", "AROUND", "ABOVE", "POSITIVE",
                                    "BELOW", "VICINITY", "GENERALLY", "CLOSE",
                                    "NOT", "SOMEWHAT", "VERY", "EXTREMELY",
                                    "SLIGHTLY", "AFTER", "BEFORE"],
                         majorDimension=2,
                         style=wx.RA_SPECIFY_COLS) 

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.Fit()
        
    def OnQuit(self,Event):
        self.Destroy()

app = wx.App(False)
frame = DemoFrame()
frame.Show()
app.MainLoop()





