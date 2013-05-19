#!/usr/bin/env python2.4

import wxversion
wxversion.select("2.6")

import wx
import  wx.stc  as  stc

class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title = "Timer Demo"):
        wx.Frame.__init__(self, None , -1, title)#, size = (800,600), style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        self.TextCtrl = stc.StyledTextCtrl(self, wx.NewId())

        self.TextCtrl.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.TextCtrl, 1, wx.GROW)
        # set up the buttons
        ButtonSizer = self.SetUpTheButtons()
        sizer.Add(ButtonSizer, 0, wx.GROW)
        self.SetSizer(sizer)

        # now set up the timer:
        self.Timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.Counter = 0

    def SetUpTheButtons(self):
        StartButton = wx.Button(self, wx.NewId(), "Start")
        StartButton.Bind(wx.EVT_BUTTON, self.OnStart)

        StopButton = wx.Button(self, wx.NewId(), "Stop")
        StopButton.Bind(wx.EVT_BUTTON, self.OnStop)

        QuitButton = wx.Button(self, wx.NewId(), "Quit")
        QuitButton.Bind(wx.EVT_BUTTON, self.OnQuit)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((1,1), 1)
        sizer.Add(StartButton, 0, wx.ALIGN_CENTER | wx.ALL, 4 )
        sizer.Add((1,1), 1)
        sizer.Add(StopButton, 0, wx.ALIGN_CENTER | wx.ALL, 4 )
        sizer.Add((1,1), 1)
        sizer.Add(QuitButton, 0, wx.ALIGN_CENTER | wx.ALL, 4 )
        sizer.Add((1,1), 1)
        return sizer

    def OnTimer(self,Event):
        self.Counter += 1
        self.TextCtrl.AddText("Sentence number: %i\n"%self.Counter)

    def OnStart(self,Event):
        self.Timer.Start(500) # time between events (in milliseconds)

    def OnStop(self, Event=None):
        self.Timer.Stop()

    def OnMouseDown(self,Event):
        if self.Timer.IsRunning():
            self.OnStop()
        else:
            Event.Skip()

    def OnQuit(self,Event):
        self.Destroy()



app = wx.PySimpleApp(0)
frame = DemoFrame()
frame.Show()
app.MainLoop()

