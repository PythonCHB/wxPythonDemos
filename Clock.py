#!/usr/bin/env python2.4

import wx
from wx.lib.analogclock import *

class MainWindow(wx.Dialog):
    """ This window displays a clock and a button """
    def __init__(self,parent,id,title):
        wx.Dialog.__init__(self, parent, id, title, size = (800,600), style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetBackgroundColour(wx.WHITE)

        clock = AnalogClockWindow(self)
        clock.SetBackgroundColour("RED")
        clock.SetHandColours("BLUE")
        clock.SetTickColours("WHITE")
        btn = wx.Button(self, wx.ID_OK, "OK")

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(clock,1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL | wx.SHAPED, 10)
        box.Add(btn,0 , wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        
        self.ShowModal()
        self.Destroy()


class MyApp(wx.App):
    def OnInit(self):

        Dw, Dh = wx.DisplaySize()
        Dw_mm, Dh_mm =  wx.DisplaySizeMM()

        Dw_i = Dw_mm / 25.4
        Dh_i = Dh_mm / 25.4

        print "The display is %i by %i pixels"%(Dw, Dh)
        print "The display is %i by %i inches"%(Dw_i, Dh_i)
        print "resulting in %i by %i ppi"%(Dw / Dw_i, Dh / Dh_i)
        
 
        frame = MainWindow(None, -1, "Clock")
        self.SetTopWindow(frame)
        
        return True
        

app = MyApp(0)
app.MainLoop()


