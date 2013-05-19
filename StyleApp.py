#!/usr/bin/env python2.4

# I like to put the python version on the #! line,
# so that I can have multiple versions installed.

"""

This is a small wxPython app developed to demonstrate how to write in
Pythonic wxPython

"""

import wx

class DemoPanel(wx.Panel):
    def __init__(self, Parent, *args, **kwargs):
        wx.Panel.__init__(self, Parent, *args, **kwargs)

        self.Parent = Parent

        NothingBtn = wx.Button(self, label="Do Nothing with a long label")
        NothingBtn.Bind(wx.EVT_BUTTON, self.DoNothing )

        MsgBtn = wx.Button(self, label="Send Message")
        MsgBtn.Bind(wx.EVT_BUTTON, self.OnMsgBtn )

        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(NothingBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        Sizer.Add(MsgBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizerAndFit(Sizer)

    def DoNothing(self, event=None):
        pass
    
    def OnMsgBtn(self, event=None):
        dlg = wx.MessageDialog(self,
                               message='A completely useless message',
                               caption='A Message Box',
                               style=(wx.OK | wx.ICON_INFORMATION)
                               )
        dlg.ShowModal()
        dlg.Destroy()

class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        # Build the menu bar
        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        
        item = FileMenu.Append(wx.ID_EXIT, text="&Quit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)

        MenuBar.Append(FileMenu, "&File")
        self.SetMenuBar(MenuBar)

        # Add the Widget Panel
        self.Panel = DemoPanel(self)

        self.Fit()

    def OnQuit(self, event=None):
        self.Close()

app = wx.App()
frame = DemoFrame(None, title="Micro App")
frame.Show()
app.MainLoop()
