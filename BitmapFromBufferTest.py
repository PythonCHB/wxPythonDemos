#!/usr/bin/env python

"""
A test of wx.BitmapFromBuffer
"""

import numpy as np
import numpy.random as random
import wx


class BitmapWindow(wx.Window):
    def __init__(self, parent, bytearray, *args, **kwargs):
        wx.Window.__init__(self, parent, *args, **kwargs)
        
        self.bytearray = bytearray
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        bmp = wx.BitmapFromBufferRGBA(200,200, self.bytearray)
        dc.DrawBitmap(bmp, 50, 0 )

class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title = "Bitmap Demo"):
        wx.Frame.__init__(self, None , -1, title)#, size = (800,600), style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        # create the array and bitmap:
        self.bytearray = np.zeros((200,200,4), dtype=np.uint8)
        self.bytearray[:,:,3] = 255

        #bmp = wx.BitmapFromBufferRGBA(200,200, self.bytearray)
        #bmp = wx.Bitmap("Images/smalltest.jpg")

        self.BitmapWindow = BitmapWindow(self, self.bytearray)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.BitmapWindow, 1, wx.GROW)
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
        print "The timer fired"
        r, g, b, a = random.randint(255, size = (4,))
        self.bytearray[:,:,0] = r
        self.bytearray[:,:,1] = g
        self.bytearray[:,:,2] = b
        self.Refresh()
        self.Update()

    def OnStart(self,Event):
        self.Timer.Start(500) # time between events (in milliseconds)

    def OnStop(self, Event=None):
        self.Timer.Stop()

    def OnQuit(self,Event):
        self.Destroy()

app = wx.PySimpleApp(0)
frame = DemoFrame()
frame.Show()
app.MainLoop()
