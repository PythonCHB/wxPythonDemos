#!/usr/bin/env python
"""
A simple sample of using a wx.Overlay to draw a rubberband effect

posted by Robin on the wxPython list.

I've added stuff for non-mac platfroms based on code posted by Chris Mellon

NOTE: something is wrong with the zooming, but the overlay works.

"""

import wx
print(wx.version())


class TestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

        self.startPos = None
        self.overlay = wx.Overlay()

    def OnPaint(self, evt):
        # Just some simple stuff to paint in the window for an example
        dc = wx.PaintDC(self)
        coords = ((40, 40), (200, 220), (210, 120), (120, 300))
        dc.SetBackground(wx.Brush("sky blue"))
        dc.Clear()

        dc.SetPen(wx.Pen("red", 2))
        dc.SetBrush(wx.CYAN_BRUSH)
        dc.DrawPolygon(coords)
        dc.DrawLabel(
            "Draw the mouse across this window to see \n"
            "a rubber-band effect using wx.Overlay", (140, 50, -1, -1))

    def OnLeftDown(self, evt):
        # Capture the mouse and save the starting posiiton for the
        # rubber-band
        self.CaptureMouse()
        self.startPos = evt.GetPosition()

    def OnMouseMove(self, evt):
        if not self.HasCapture():
            return
        rect = wx.Rect(self.startPos, evt.GetPosition())
        # Draw the rubber-band rectangle using an overlay so it
        # will manage keeping the rectangle and the former window
        # contents separate.
        dc = wx.ClientDC(self)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()

        pen = wx.Pen("black", 2)
        brush = wx.Brush(wx.Colour(192, 192, 192, 128))
        if "wxMac" in wx.PlatformInfo:
            dc.SetPen(pen)
            dc.SetBrush(brush)
            dc.DrawRectangle(rect)
        else:
            # use a GC on Windows (and GTK?)
            # this doesn't work on the Mac
            ctx = wx.GraphicsContext.Create(dc)
            ctx.SetPen(pen)
            ctx.SetBrush(brush)
            print("drawing:", rect)
            ctx.DrawRectangle(*rect)

        del odc  # work around a bug in the Python wrappers to make
        # sure the odc is destroyed before the dc is.

    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
        self.startPos = None

        # When the mouse is released we reset the overlay and it
        # restores the former content to the window.
        dc = wx.ClientDC(self)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        del odc
        self.overlay.Reset()


if __name__ == "__main__":
    app = wx.App(redirect=False)
    frm = wx.Frame(None, title="wx.Overlay Test", size=(450, 450))
    #work around flicker on MSW - setting transparency
    #turns on window compositing, which allows for buffering
    #of clientDC drawing
    if "wxMSW" in wx.PlatformInfo:
        frm.SetTransparent(254)
    pnl = TestPanel(frm)
    frm.Show()
    app.MainLoop()
