#!/usr/bin/env python

"""
a small test of initializing a wxImage from a numpy array
"""


import wx
import numpy as N
import numpy.random as rand


class ImagePanel(wx.Panel):
    """
    A very simple panel for displaying a wx.Image
    """
    def __init__(self, image, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.image = image
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(wx.BitmapFromImage(self.image), 0, 0)


class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title = "Micro App"):
        wx.Frame.__init__(self, None , -1, title)

        MenuBar = wx.MenuBar()
        FileMenu = wx.Menu()

        item = FileMenu.Append(wx.ID_ANY, text="&Open")
        self.Bind(wx.EVT_MENU, self.OnOpen, item)

        item = FileMenu.Append(wx.ID_PREFERENCES, text="&Preferences")
        self.Bind(wx.EVT_MENU, self.OnPrefs, item)

        item = FileMenu.Append(wx.ID_EXIT, text="&Exit")
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

        btn = wx.Button(self, label="NewImage")
        btn.Bind(wx.EVT_BUTTON, self.OnNewImage)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        ##Create numpy array, and image from it
        w = h = 200
        self.array = rand.randint(0, 255, (3, w, h)).astype('uint8')
        print(self.array)
        image = wx.ImageFromBuffer(w, h, self.array)
        #image = wx.Image("Images/cute_close_up.jpg")
        self.Panel = ImagePanel(image, self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add(self.Panel, 1, wx.GROW)

        self.SetSizer(sizer)

    def OnNewImage(self, event=None):
        """
        create a new image by changing underlying numpy array
        """
        self.array *= 1.2
        self.Panel.Refresh()

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


if __name__ == "__main__" :
    app = wx.App(False)
    frame = DemoFrame()
    frame.Show()
    app.MainLoop()
