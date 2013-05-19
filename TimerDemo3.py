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

        # now set up the timers:
        self.Timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer1, self.Timer1) 
        #self.Bind(wx.EVT_TIMER, self.OnTimer1, id = self.Timer1.GetId()) 
        #self.Timer1.Bind(wx.EVT_TIMER, self.OnTimer1)

        self.Timer2 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer2, self.Timer2)
        #self.Bind(wx.EVT_TIMER, self.OnTimer2, id = self.Timer2.GetId())
        #self.Timer2.Bind(wx.EVT_TIMER, self.OnTimer2)

        self.Counter1 = 0
        self.Counter2 = 0

    def SetUpTheButtons(self):
        StartButton1 = wx.Button(self, wx.NewId(), "Start1")
        StartButton1.Bind(wx.EVT_BUTTON, self.OnStart1)

        StartButton2 = wx.Button(self, wx.NewId(), "Start2")
        StartButton2.Bind(wx.EVT_BUTTON, self.OnStart2)

        StopButton = wx.Button(self, wx.NewId(), "Stop")
        StopButton.Bind(wx.EVT_BUTTON, self.OnStop)

        QuitButton = wx.Button(self, wx.NewId(), "Quit")
        QuitButton.Bind(wx.EVT_BUTTON, self.OnQuit)

        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((1,1), 1)
        sizer.Add(StartButton1, 0, wx.ALIGN_CENTER | wx.ALL, 4 )
        sizer.Add((1,1), 1)
        sizer.Add(StartButton2, 0, wx.ALIGN_CENTER | wx.ALL, 4 )
        sizer.Add((1,1), 1)
        sizer.Add(StopButton, 0, wx.ALIGN_CENTER | wx.ALL, 4 )
        sizer.Add((1,1), 1)
        sizer.Add(QuitButton, 0, wx.ALIGN_CENTER | wx.ALL, 4 )
        sizer.Add((1,1), 1)
        return sizer

    def OnTimer1(self,Event):
        print "OnTimer1 called"
        self.Counter1 += 1
        self.TextCtrl.AddText("Timer1 Output: %i\n"%self.Counter1)

    def OnStart1(self,Event):
        self.Timer1.Start(200) # time between events (in milliseconds)

    def OnTimer2(self,Event):
        print "OnTimer2 called"
        self.Counter2 += 1
        self.TextCtrl.AddText("Timer2 Output: %i\n"%self.Counter2)

    def OnStart2(self,Event):
        self.Timer2.Start(1000) # time between events (in milliseconds)

    def OnStop(self, Event=None):
        self.Timer1.Stop()
        self.Timer2.Stop()

    def OnMouseDown(self,Event):
        if self.Timer1.IsRunning():
            self.OnStop()
        else:
            Event.Skip()

    def OnQuit(self,Event):
        self.Destroy()



app = wx.PySimpleApp(0)
frame = DemoFrame()
frame.Show()
app.MainLoop()

