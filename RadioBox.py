#!/usr/bin/env python2.4

import wx

class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title = "Micro App"):
        wx.Frame.__init__(self, None , -1, title)#, size = (800,600), style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        
        item = wx.MenuItem(FileMenu, wx.ID_ANY, "&Quit")
        FileMenu.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnQuit, item)

        MenuBar.Append(FileMenu, "&File")
        self.SetMenuBar(MenuBar)


        RB = wx.RadioBox(self,
                         -1,
                         "Hedges",
                         wx.DefaultPosition,
                         wx.DefaultSize,
                         ["ABOUT", "AROUND", "ABOVE", "POSITIVE", "BELOW",
                          "VICINITY", "GENERALLY", "CLOSE", "NOT", "SOMEWHAT", "VERY", "EXTREMELY",
                          "SLIGHTLY", "AFTER", "BEFORE"],
                         2,
                         wx.RA_SPECIFY_COLS) 

        wx.EVT_CLOSE(self,self.OnQuit)

        self.Fit()
        
    def OnQuit(self,Event):
        self.Destroy()

app = wx.PySimpleApp(0)
frame = DemoFrame()
frame.Show()
app.MainLoop()





