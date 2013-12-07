#!/usr/bin/env python

import os
import sys
import wx


class MyPanel(wx.Panel):
    def __init__(self, frame, id):
        wx.Panel.__init__(self, frame, id)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.count = 0
        # make a buffer for the text
        # you could do better by using DC.GetTextExtent()
        # or buffer the whole Panel
        # see the Double Buffer page in the wxPython Wiki
        dc = wx.ClientDC(self)# I need a DC to get the text size
        dc.SetFont(self.font)
        #dc.GetTextExtent("count: XXXX")# big enough for 4 digits
        self.TextBuffer = wx.EmptyBitmap(*dc.GetTextExtent("count: XXXX"))

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("white"))
        dc.Clear()
        self.drawText(dc)

    def OnMouseMove(self, event):
        if event.Dragging():
            self.count = self.count + 1
            self.drawText()

    def drawText(self, dc=None):
        if dc is None:
            dc = wx.ClientDC(self)
        mdc = wx.MemoryDC()## you could keep this around, but I think that
                           ## can cause problems on older Windows systems.
        mdc.SelectObject(self.TextBuffer)
        mdc.SetBackground(wx.Brush("white"))
        mdc.Clear()
        mdc.SetFont(self.font)
        txt = "count: %i"%(self.count)
        mdc.DrawText(txt, 0, 0)

        del mdc # delete the Memdc , so that I can draw the bitmap on Windows
        dc.DrawBitmap(self.TextBuffer,20,20)

        ## Blit is another option, but you can see that it's harder to
        ## use for hte simple case.
        #dc.Blit(20, 20, self.TextBuffer.GetWidth(), self.TextBuffer.GetHeight(), mdc, 0, 0)

        return None


class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, pos=(150, 150), size=(500, 400))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.iPanel = MyPanel(self, -1)

    def OnCloseWindow(self, event):
        self.Destroy()


class MyApp(wx.App):
    def OnInit(self):
        msg = "drag with left mouse button to increment numbers"
        frame = MyFrame(None, -1, msg)
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
