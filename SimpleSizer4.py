#!/usr/bin/env python2.3

import wx

class TestFrame(wx.Frame):
    def __init__(self, parent, ID, title = ""):
        wx.Frame.__init__(self, parent, -1, title, style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        

        # Amount/Cleared Row
        Space = 4
        self.amountrow = wx.BoxSizer(wx.HORIZONTAL)

        self.amountrow.Add(wx.StaticText(self,-1,"Amount"), 0, wx.ALL, Space)

        self.amount = wx.TextCtrl(self,-1,"",size=wx.Size(80,-1))
        self.amountrow.Add(self.amount, 1, wx.ALL, Space)

        self.cleared = wx.CheckBox(self,-1,"Cleared")
        self.amountrow.Add(self.cleared, 0, wx.ALIGN_RIGHT | wx.ALL, Space)

        self.vbox.Add(self.amountrow, 0, wx.EXPAND | wx.ALL, Space)
        
        # Memo/Button box
        self.buttonrow = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonrow.Add(wx.StaticText(self,-1,"Memo"), 0, wx.ALL, Space)
        self.memo = wx.TextCtrl(self,-1,"",size=wx.Size(80,-1))
        self.buttonrow.Add(self.memo, 0, wx.ALL, Space)
        self.ok_button = wx.Button(self,wx.ID_OK,"OK")
        self.ok_button.SetDefault()
        self.cancel_button = wx.Button(self,wx.ID_CANCEL,"Cancel")
        self.buttonrow.Add(self.ok_button, 0, wx.ALL, Space)
        self.buttonrow.Add(self.cancel_button, 0, wx.ALL, Space)
        self.vbox.Add(self.buttonrow, 0, wx.ALL, Space)

        self.vbox.Layout()
        self.SetSizerAndFit(self.vbox)

        return True
        
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
     











