#!/usr/bin/env

import wx
if wx.Platform == '__WXMSW__':
    import wx.lib.iewin as iewin
else:
    raise ImporrError("This test only works on windows")

class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title = "Micro App"):
        wx.Frame.__init__(self, None , -1, title)


        btn = wx.Button(self, label = "Get HTML")
        btn.Bind(wx.EVT_BUTTON, self.GetHTML )
        self.Bind(wx.EVT_CLOSE, self.GetHTML)

        self.htwin = iewin.IEHtmlWindow(self)
        self.htwin.Navigate('http://cameochemicals.noaa.gov/')
        
        S = wx.BoxSizer(wx.VERTICAL)
        S.Add(btn, 0, wx.ALL, 5)
        S.Add(self.htwin, 1, wx.EXPAND)
        self.SetSizer(S)
        self.SetSize((700,500))

        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        
    def OnQuit(self,Event):
        self.Destroy()

    def GetHTML(self, event=None):
        print "contents of HTML window as text: ", self.htwin.GetText(asHTML=False)[:500]
        print "contents of HTML window as html: ", self.htwin.GetText(asHTML=True)

app = wx.App(False)
frame = DemoFrame()
frame.Show()
app.MainLoop()





