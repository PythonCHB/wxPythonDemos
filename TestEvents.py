#!/usr/bin/env python
"""

A very simple app for testing DC and mouse event functionality

"""


import wx

class TestPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs) 
                          
 
        wx.EVT_PAINT(self, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN , self.LeftDown)
        self.Bind(wx.EVT_LEFT_UP , self.LeftUp)
        self.Bind(wx.EVT_MOTION, self.Move)

        ##This would capture all events in the same handler
        #wx.EVT_MOUSE_EVENTS(self, self.OnMouseEvents)


    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.BeginDrawing()
        dc.Clear()

        dc.DrawText("Text", 50, 50 )
        dc.EndDrawing()

    def OnMouseEvents(self,event):
        if event.IsButton():
            print event.GetButton()

    def LeftDown(self, event):
        print "In LeftDown, at:", event.Position
        
    def LeftUp(self, event):
        print "In LeftUp at:", event.Position
        
    def Move(self, event):
        print "In Motion event at:", event.Position
  
class DemoApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None,
                         title="Mouse Event Test",
                         size=(200,200),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE,
                         )
        print type(frame)
        panel = TestPanel(frame)

        frame.Show(True)

        return True

if __name__ == "__main__":
    app = DemoApp(False)
    app.MainLoop()



















