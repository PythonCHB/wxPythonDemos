#!/usr/bin/env python

"""
A test of temporatry drawing using a method called from OnPaint

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
    SaveToFile(self,file_name,file_type) method.

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

    def TempDraw(self, dc):
        """
        This is where youput stuff that you want draw temporarily on top
        of the buffer, like during Mouse actions, etc.
        """
        pass

    def OnPaint(self, event):
        print("In OnPaint")
        # All that is needed here is to draw the buffer to screen
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self._Buffer, 0, 0)
        self.TempDraw(dc)

    def OnSize(self,event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size = self.GetClientSizeTuple()

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
        wx.ClientDC(self).DrawBitmap(self._Buffer, 0, 0)


class DrawWindow(BufferedWindow):
    def __init__(self, parent, id=-1):
        ## Any data the Draw() function needs must be initialized before
        ## calling BufferedWindow.__init__, as it will call the Draw
        ## function.
        BufferedWindow.__init__(self, parent, id)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMove)

        self.StartMove = None

        self.overlay = wx.Overlay()

    def OnLeftDown(self, event):
        self.CaptureMouse()
        self.StartMove = event.GetPosition()

    def OnLeftUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
        self.StartMove = None
        #self.Refresh()
        # When the mouse is released we reset the overlay and it
        # restores the former content to the window.
        #dc = wx.ClientDC(self)
        #odc = wx.DCOverlay(self.overlay, dc)
        #odc.Clear()
        #del odc
        self.overlay.Reset()

    def OnMove(self, event):
        if event.Dragging() and event.LeftIsDown() and self.StartMove is not None:
            pos = event.GetPosition()
            #self.Refresh()
            dc = wx.ClientDC(self)
            odc = wx.DCOverlay( self.overlay, dc)
            odc.Clear()
            ## a black and white line so you can see it over any color.
            dc.SetPen(wx.Pen('WHITE', 2))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawLinePoint(self.StartMove, pos)
            dc.SetPen(wx.Pen('BLACK', 2, wx.PENSTYLE_SHORT_DASH))
            dc.DrawLinePoint(self.StartMove, pos)

            del odc # to ensure it gets delted before the Client

    def Draw(self, dc):
        coords = ((40, 40), (200, 220), (210, 120), (120, 300))
        dc.BeginDrawing()
        dc.SetBackground(wx.Brush("Blue"))
        dc.Clear() # make sure you clear the bitmap!

        dc.SetPen(wx.RED_PEN)
        dc.SetBrush(wx.CYAN_BRUSH)

        dc.DrawPolygon(coords)


class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.Window = DrawWindow(self)


class DemoApp(wx.App):
    def OnInit(self):
        frame = TestFrame(None, title="OverlayTest", size=(500, 500))
        frame.Show(True)

        self.SetTopWindow(frame)

        return True


if __name__ == "__main__":
    app = DemoApp(0)
    app.MainLoop()
