#!/usr/bin/env python

"""
A test of using a ClientDC to draw while the mosue is moving
"""

import wx
print(wx.version())
import random


class BufferedWindow(wx.Window):
    """

    A Buffered window class.

    To use it, subclass it and define a Draw(DC) method that takes a DC
    to draw to. In that method, put the code needed to draw the picture
    you want. The window will automatically be double buffered, and the
    screen will be automatically updated when a Paint event is received.

    When the drawing needs to change, you app needs to call the
    UpdateDrawing() method. Since the drawing is stored in a bitmap, you
    can also save the drawing to file by calling the
    SaveToFile(self, file_name, file_type) method.

    """
    def __init__(self, parent, id,
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.NO_FULL_REPAINT_ON_RESIZE):
        wx.Window.__init__(self, parent, id, pos, size, style)

        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)

    def Draw(self, dc):
        ## just here as a place holder.
        ## This method should be over-ridden when subclassed
        pass

    def OnPaint(self, event):
        # All that is needed here is to draw the buffer to screen
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self._Buffer, 0, 0)

    def OnSize(self,event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size  = self.GetClientSizeTuple()

        # Make sure we don't try to create a 0 size bitmap
        Size = (max(Size[0], 1), max(Size[1], 1))
        self._Buffer = wx.EmptyBitmap(Size[0], Size[1])
        self.UpdateDrawing()

    def SaveToFile(self, FileName, FileType):
        ## This will save the contents of the buffer
        ## to the specified file. See the wxWindows docs for
        ## wx.Bitmap::SaveFile for the details
        self._Buffer.SaveFile(FileName, FileType)

    def UpdateDrawing(self):
        """
        This would get called if the drawing needed to change, for whatever reason.

        The idea here is that the drawing is based on some data generated
        elsewhere in the system. IF that data changes, the drawing needs to
        be updated.

        """

        # update the buffer
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.Draw(dc)
        # update the screen
        wx.ClientDC(self).DrawBitmap(self._Buffer,0,0)


class DrawWindow(BufferedWindow):
    def __init__(self, parent, id = -1):
        ## Any data the Draw() function needs must be initialized before
        ## calling BufferedWindow.__init__, as it will call the Draw
        ## function.
        BufferedWindow.__init__(self, parent, id)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMove)

        self.StartMove = None
        self.PrevMove = None

    def OnLeftDown(self, event):
        self.CaptureMouse()
        self.StartMove = event.GetPosition()
        self.PrevMove = None

    def OnLeftUp(self, event):
        if self.PrevMove is not None:
            self.DrawLine(event, New=False)
        self.StartMove = None
        self.PrevMove = None

    def OnMove(self, event):
        if event.Dragging() and event.LeftIsDown() and self.StartMove is not None:
            self.DrawLine(event)

    def DrawLine(self, event, New=True):
        dc = wx.ClientDC(self)
        dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetLogicalFunction(wx.INVERT)
        if self.PrevMove is not None:
            print("Drawing Over old line:", self.StartMove, self.PrevMove)
            dc.DrawLinePoint(self.StartMove, self.PrevMove)
        self.PrevMove = event.GetPosition()
        print("Drawing new line:", self.StartMove, self.PrevMove)
        if New:
            dc.DrawLinePoint( self.StartMove, self.PrevMove )

    def Draw(self, dc):
        coords = ((40,40),(200,220),(210,120),(120,300))
        dc.BeginDrawing()
        dc.SetBackground( wx.Brush("Blue") )
        dc.Clear() # make sure you clear the bitmap!

        dc.SetPen(wx.RED_PEN)
        dc.SetBrush(wx.CYAN_BRUSH)

        dc.DrawPolygon(coords)


class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "ClientDC Test",
                         wx.DefaultPosition,
                         size=(500, 500),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        self.Window = DrawWindow(self)
        self.Window.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.Centre()

    def OnKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()


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
