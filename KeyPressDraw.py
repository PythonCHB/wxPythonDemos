#!/usr/bin/env python2.4
 
import wx

class DrawPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=0)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Refresh()

    def OnPaint(self, event=None):

        print "In Paint Event"
        print PressedKey_instance.a_key_is_pressed
        
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen("RED", 4))
              
        if PressedKey_instance.a_key_is_pressed == 'TRUE':
            dc.DrawLine(0, 0, 1000, 0)
           
            PressedKey_instance.a_key_is_pressed = 'FALSE'
            print PressedKey_instance.a_key_is_pressed
       
       

class PressedKey(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=0)
        self.Bind(wx.EVT_CHAR, self.LogKeyEvent)
        self.SetFocus()

        self.a_key_is_pressed = 'FALSE'
    def LogKeyEvent(self, evt):
        self.a_key_is_pressed = 'TRUE'
        print self.a_key_is_pressed


class MyApp(wx.App):
    def OnInit(self):
        frame1 = wx.Frame(None, -1, "Draw A Line", pos=(0,0), size=(400,300))
        frame2 = wx.Frame(None, -1, "Keep Focus!", pos=(400,300), size=(410,310))
       
        global PressedKey_instance
        PressedKey_instance = PressedKey(frame2)
       
        DrawPanel(frame1)
       
        frame1.Show(True)
        frame2.Show(True)
        return True


app = MyApp(0)
app.MainLoop()
