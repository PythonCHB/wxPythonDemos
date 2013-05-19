#!/usr/bin/env python2.4

import wx
        
class MyApp(wx.App):
    def OnInit(self):

        Dw, Dh = wx.DisplaySize()
        Dw_mm, Dh_mm =  wx.DisplaySizeMM()

        Dw_i = Dw_mm / 25.4
        Dh_i = Dh_mm / 25.4

        print "The display is %i by %i pixels"%(Dw, Dh)
        print "The display is %i by %i inches"%(Dw_i, Dh_i)
        print "resulting in %i by %i ppi"%(Dw / Dw_i, Dh / Dh_i)

        dc = wx.ScreenDC()
        print " The system reports : %s PPI"%dc.GetPPI()

        return True
        

app = MyApp(0)
app.MainLoop()





