#!/usr/bin/env python

import wx
print("wxPython version:", wx.version())


class OverlayPanel(wx.Panel):
    def __init__(self, parent):
        super(OverlayPanel, self).__init__(parent)
        self.overlay = wx.Overlay()
        self.permRect = None
        self.selectionStart = None
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        if self.permRect:
            dc.SetBrush(wx.BLACK_BRUSH)
            if 'phoenix' in wx.version():
                dc.DrawRectangle(self.permRect)
            else:
                dc.DrawRectangleRect(self.permRect)

    def OnLeftDown(self, evt):
        self.CaptureMouse()
        self.overlay = wx.Overlay()
        self.selectionStart = evt.Position

    def OnLeftUp(self, evt):
        if not self.HasCapture():
            return
        self.ReleaseMouse()
        if 'phoenix' in wx.version():
            self.permRect = wx.Rect(self.selectionStart, evt.Position)
        else:
            self.permRect = wx.RectPP(self.selectionStart, evt.Position)
        self.selectionStart = None
        #clear out any existing drawing
        self.overlay.Reset()
        self.Refresh()

    def OnMotion(self, evt):
        if not self.HasCapture():
            return

        dc = wx.ClientDC(self)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        if 'phoenix' in wx.version():
            ctx = wx.GraphicsContext.Create(dc)
        else:
            ctx = wx.GraphicsContext_Create(dc)
        ctx.SetPen(wx.GREY_PEN)
        ctx.SetBrush(wx.Brush(wx.Colour(192, 192, 192, 128)))
        if 'phoenix' in wx.version():
            ctx.DrawRectangle(self.selectionStart[0], self.selectionStart[0], evt.Position[0], evt.Position[1])
        else:
            ctx.DrawRectangle(*wx.RectPP(self.selectionStart, evt.Position))
        del odc


if __name__ == '__main__':
    app = wx.App(False)
    f = wx.Frame(None)
    #work around flicker on MSW - setting transparency
    #turns on window compositing, which allows for buffering
    #of clientDC drawing
    f.SetTransparent(254)
    p = OverlayPanel(f)
    f.Show()
    app.MainLoop()
