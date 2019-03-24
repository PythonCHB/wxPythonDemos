#!/usr/bin/env python

# multibox.py -- in a frame

import wx


class MyPanel(wx.Panel):
    def __init__(self, parent, ID=wx.ID_ANY, size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, ID, size)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # Top row:
        stName = wx.StaticText(self, -1, "Model name:")
        tName  = wx.TextCtrl(self, -1, "", style=wx.TE_LEFT |
                                                 wx.TAB_TRAVERSAL |
                                                 wx.RAISED_BORDER)
        hbox1.Add(stName, 0, wx.ALL, 0)
        hbox1.Add(tName, 1, wx.ALL, 2)

        stDesc = wx.StaticText(self, -1, "Model description:")
        tDesc = wx.TextCtrl(self, -1,
                            style=wx.TAB_TRAVERSAL | wx.TE_MULTILINE |
                                  wx.TE_LINEWRAP | wx.RAISED_BORDER |
                                  wx.HSCROLL, name="modDesc")
        hbox1.Add(stDesc, 0, wx.ALL, 2)
        hbox1.Add(tDesc, 2, wx.EXPAND | wx.ALL, 0)

        vbox1.Add(hbox1, 1, wx.EXPAND | wx.ALL, 5)

        # Middle row
        vbox1.Add(wx.RadioBox(self, -1, choices=['Fuzzy reasoning', 'Backward chaining',
                                                 'Forward chaining'],
                              majorDimension=3, size=(420, 45),
                              style=wx.RAISED_BORDER | wx.RA_SPECIFY_COLS,
                              label='Model Type'), 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # Bottom row
        vbox1.Add(wx.StaticBox(self, -1, label='Consequent Fuzzy Set',
                  style=wx.RAISED_BORDER), 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(vbox1)
        self.Layout()

    ## Here you put the functionality of how the controls work together.

class MyFrame(wx.Frame):
     def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title='Test Multiboxes')

        panel = MyPanel(self, size=(700, 500))

        self.Fit()


class MyApp(wx.App):
    def OnInit(self):
        self.main = MyFrame(None, -1, "")
        self.main.Show()
        self.SetTopWindow(self.main)
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

