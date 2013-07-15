#!/usr/bin/env python

"""
A test of drawing while the mouse is moving.

The old way of doing this is with a wxClientDC, but that does
not work right, or at least not well on OS-X. So this shows how
to do it with Refresh();Update().
"""

import wx

print "running with version:", wx.__version__
import random


class DrawWindow(wx.Panel):
    def __init__(self, parent, id = -1):
        ## Any data the Draw() function needs must be initialized before
        ## calling BufferedWindow.__init__, as it will call the Draw
        ## function.
        wx.Panel.__init__(self, parent, id)
        
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMove)

        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.

        self.mouse_line = None
        self.OnSize(None)

    def OnPaint(self, event):
        # This draws the buffer to the screen, then optionally the mouse_line
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self._Buffer,0,0)
        if self.mouse_line is not None:
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.DrawLinePoint( *self.mouse_line )


    def OnSize(self,event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size  = self.GetClientSizeTuple()

        # Make sure we don't try to create a 0 size bitmap
        Size = (max(Size[0], 1), max(Size[1], 1))
        self._Buffer = wx.EmptyBitmap(Size[0],Size[1])
        self.Draw()

    def Draw(self):
        """
        This draws the backgound image on the buffer

        """
        # update the buffer
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)

        coords = ((40,40),(200,220),(210,120),(120,300))
        dc.BeginDrawing()
        dc.SetBackground( wx.Brush("Blue") )
        dc.Clear() # make sure you clear the bitmap!

        dc.SetPen(wx.RED_PEN)
        dc.SetBrush(wx.CYAN_BRUSH)

        dc.DrawPolygon(coords)


    def OnLeftDown(self, event):
        self.CaptureMouse()
        self.mouse_line = [ event.GetPosition(), None]

    def OnLeftUp(self, event):
        self.mouse_line = None
        if self.HasCapture():
            self.ReleaseMouse()
        self.Refresh()
        self.Update()

    def OnMove(self, event):
        if event.Dragging() and event.LeftIsDown() and (self.mouse_line is not None):
            self.mouse_line[1] = event.GetPosition()
        self.Refresh()
        self.Update()


class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "ClientDC Test",
                         wx.DefaultPosition,
                         size=(500,500),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        self.Window = DrawWindow(self)

class DemoApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers() # called so a PNG can be saved      
        frame = TestFrame()
        frame.Show(True)

        ## initialize a drawing
        ## It doesn't seem like this should be here, but the Frame does
        ## not get sized untill Show() is called, so it doesn't work if
        ## it is put in the __init__ method.

        #frame.NewDrawing(None)

        self.SetTopWindow(frame)

        return True

if __name__ == "__main__":
    app = DemoApp(0)
    app.MainLoop()




















