#!/usr/bin/env python

import wx


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        NumButtons = 6

        MainSizer = wx.BoxSizer(wx.HORIZONTAL)

        ## The lambda trick:
        ButtonSizer = wx.StaticBoxSizer(wx.StaticBox(self,label="lambda trick"),
                                        wx.VERTICAL)
        for i in range(NumButtons):
            b = wx.Button(self, label= str(i))
            b.Bind(wx.EVT_BUTTON, lambda evt, num=i: self.OnClick(evt, num))
            ButtonSizer.Add(b, 0, wx.EXPAND|wx.ALL, 10)
        MainSizer.Add(ButtonSizer)
        
        ## Using the label:
        ButtonSizer = wx.StaticBoxSizer(wx.StaticBox(self,label="Using the label"),
                                        wx.VERTICAL)
        for i in range(NumButtons):
            b = wx.Button(self, label= str(i))
            b.Bind(wx.EVT_BUTTON, self.OnClick2)
            ButtonSizer.Add(b, 0, wx.EXPAND|wx.ALL, 10)
        MainSizer.Add(ButtonSizer)

        ## Storing the ID:
        ButtonSizer = wx.StaticBoxSizer(wx.StaticBox(self,label="Storing the ID"),
                                        wx.VERTICAL)
        self.ButtonIDs = {}
        for i in range(NumButtons):
            b = wx.Button(self, label= str(i))
            self.ButtonIDs[b.Id] = i
            b.Bind(wx.EVT_BUTTON, self.OnClick3)
            ButtonSizer.Add(b, 0, wx.EXPAND|wx.ALL, 10)
        MainSizer.Add(ButtonSizer)

        ## Using FindWinowById():
        ButtonSizer = wx.StaticBoxSizer(wx.StaticBox(self,label="FindWinowById()"),
                                        wx.VERTICAL)
        for i in range(NumButtons):
            b = wx.Button(self, label= str(i))
            b.Bind(wx.EVT_BUTTON, self.OnClick4)
            # add an arbitrary attribute
            b.myData = "This is button %i"%i
            ButtonSizer.Add(b, 0, wx.EXPAND|wx.ALL, 10)
        MainSizer.Add(ButtonSizer)

        self.SetSizerAndFit(MainSizer)
    
    def OnClick(self, evt, num):
        print "Button %i Clicked"%num

    def OnClick2(self, evt):
        but = evt.GetEventObject()
        print "Button %s Clicked"%but.Label

    def OnClick3(self, evt):
        but = self.ButtonIDs[evt.Id]
        print "Button %s Clicked"%but

    def OnClick4(self, evt):
        but = wx.FindWindowById(evt.Id)
        print "Button %s Clicked"%but.myData


    
App = wx.App(False)
F = MyFrame(None, title="Test Frame")
F.Show()
App.MainLoop()


        
    
