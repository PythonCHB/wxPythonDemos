#!/usr/bin/env python

import wx
from wx import webview

class DemoFrame(wx.Frame):
    """ This window displays a WebKit window """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.WKWindow = webview.WebView(self)
        self.WKWindow.LoadURL("http://www.google.com")
        #self.WKWindow = webkit.WebKitCtrl(self)
        #self.WKWindow = wx.Panel(self)
        #self.WKWindow.SetBackgroundColour("red")
    
        self.Bind(webview.EVT_WEBVIEW_NEW_WINDOW, self.OnNewWindow)
        #self.Fit()
        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        
        item = FileMenu.Append(wx.ID_ANY, text = "&Open")

        self.Bind(wx.EVT_MENU, self.OnOpen, item)

        item = FileMenu.Append(wx.ID_PREFERENCES, text = "&Preferences")
        self.Bind(wx.EVT_MENU, self.OnPrefs, item)

        item = FileMenu.Append(wx.ID_EXIT, text = "&Exit")

        self.Bind(wx.EVT_MENU, self.OnQuit, item)


        MenuBar.Append(FileMenu, "&File")
        
        HelpMenu = wx.Menu()

        item = HelpMenu.Append(wx.ID_HELP, "Test &Help",
                                "Help for this simple test")
        self.Bind(wx.EVT_MENU, self.OnHelp, item)

        ## this gets put in the App menu on OS-X
        item = HelpMenu.Append(wx.ID_ABOUT, "&About",
                                "More information About this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        MenuBar.Append(HelpMenu, "&Help")

        self.SetMenuBar(MenuBar)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

    def OnNewWindow(self, evt):
        print "NewWindow"
    def OnQuit(self,Event):
        self.Destroy()
        
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small program to test\n"
                                     "the use of menus on Mac, etc.\n",
                                "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnHelp(self, event):
        dlg = wx.MessageDialog(self, "This would be help\n"
                                     "If there was any\n",
                                "Test Help", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnOpen(self, event):
        dlg = wx.MessageDialog(self, "This would be an open Dialog\n"
                                     "If there was anything to open\n",
                                "Open File", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnPrefs(self, event):
        dlg = wx.MessageDialog(self, "This would be an preferences Dialog\n"
                                     "If there were any preferences to set.\n",
                                "Preferences", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

app = wx.App(False)
frame = DemoFrame(None, title="WebKit test", size=(500,500))
frame.Show()
app.MainLoop()

