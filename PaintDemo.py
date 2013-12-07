#!/usr/bin/env python

import wx
from random import randint


class MyPanel(wx.Panel):
    def __init__(self, parent, size, position):
        wx.Panel.__init__(self, parent, -1, size=size, pos=position)
        self.NewShape()

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawRectangle(*self.shape)

    def NewShape(self):
        shapeSz = randint(50, 100)
        sz = self.GetSize()
        self.shape = (randint(0, sz[0] - shapeSz),
                     randint(0, sz[1] - shapeSz),
                     shapeSz, shapeSz)

    def DrawShape(self):
        dc = wx.ClientDC(self)
        dc.Clear()

        for i in range(randint(0, 6)):
            self.NewShape()
            dc.SetBrush(wx.Brush(wx.Colour(randint(0, 255),
                                           randint(0, 255),
                                           randint(0, 255),
                                           255)))
            r = randint(0, 5)
            if r == 0:
                dc.DrawCircle(self.shape[0], self.shape[1], self.shape[2])
            elif r == 1:
                dc.DrawRectangle(*self.shape)
            elif r == 2:
                dc.SetFont(wx.Font(24, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                dc.DrawRotatedText('(%s, %s)' %(self.shape[0], self.shape[1]),
                                   self.shape[0], self.shape[1],
                                   float(randint(0, 360)))
            elif r == 3:
                dc.DrawRoundedRectangle(*self.shape, radius=float(randint(0, 20)))
            elif r == 4:
                dc.GradientFillLinear(wx.Rect(*self.shape),
                        initialColour=wx.Colour(randint(0, 255), randint(0, 255), randint(0, 255), 255),
                        destColour=wx.Colour(randint(0, 255), randint(0, 255), randint(0, 255), 255))
            elif r == 5:
                dc.GradientFillConcentric(wx.Rect(*self.shape),
                        initialColour=wx.Colour(randint(0, 255), randint(0, 255), randint(0, 255), 255),
                        destColour=wx.Colour(randint(0, 255), randint(0, 255), randint(0, 255), 255),
                        circleCenter=(self.shape[0], self.shape[1]))


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        button = wx.Button(self, -1, label="Add New")
        button.Bind(wx.EVT_BUTTON, self.UpdatePanel)

        self.Panel = MyPanel(self, (200, 200), (100, 250))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(self.Panel, 1, wx.EXPAND)

        self.SetSizer(sizer)

    def UpdatePanel(self,event):
        self.Panel.DrawShape()


if __name__ == '__main__':
    app = wx.App(0)
    frame = MyFrame(None, title="Test", size=(500, 500))
    frame.Show()
    app.MainLoop()
