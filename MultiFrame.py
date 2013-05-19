#!/usr/bin/env python

"""
A demo of how to do really simple communication between multiple frames
"""

import wx
import random

class MsgFrame(wx.Frame):
    """ This window displays a simple message """
    def __init__(self, frame_num):
        wx.Frame.__init__(self, None, -1, title="Frame # %i"%frame_num, size=(400,100))

        self.frame_num = frame_num
        self.message = wx.StaticText(self, label = "A non-message")
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add((1,1), 1)
        s.Add(self.message, 0, wx.ALIGN_CENTER)
        s.Add((1,1), 1)
        
        self.SetSizer(s)
        
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)

    def SetMessage(self, message):
        self.message.Label = message
        self.Layout()
        self.Refresh()
        self.Update()

    def OnClick(self, evt):
        pos = evt.Position
        App = wx.GetApp()
        App.SetMessage("Mouse clicked in frame: %i at position: (%i, %i)"%(self.frame_num, pos[0], pos[1]), self.frame_num+1)

class DemoApp(wx.App):

    def OnInit(self):
        
        # build the frames:
        self.frames = []
        for i in range(5):
            frame = MsgFrame(frame_num=i)
            frame.Move((30+i*100, 30+i*100))
            frame.Show()
            self.frames.append(frame)
        
        return True
        
    def SetMessage(self, message, frame_num):
        """ set a message on the given frame_number """
        try:
            self.frames[frame_num].SetMessage(message)
        except IndexError:
            self.frames[0].SetMessage(message)


app = DemoApp(False)
app.MainLoop()





