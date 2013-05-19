#!/usr/bin/env python2.3

import wx

class MainWindow(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self, parent , -1, title)#, size = (800,600), style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        wx.EVT_MOUSEWHEEL(self, self.OnWheel)
        
    def OnQuit(self,Event):
        self.Destroy()

    def OnWheel(self, event):
        print "Mouse Wheel Moved in Frame"
        print "Wheel Rotation is:", event.GetWheelRotation()
        print "Wheel Delta is:", event.GetWheelDelta()

class MyApp(wx.App):
    def OnInit(self):
        frame = MainWindow(None, -1, "Micro App")
        self.SetTopWindow(frame)
        frame.Show()
        
        return True
        

app = MyApp(0)
app.MainLoop()





