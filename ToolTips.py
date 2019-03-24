#!/usr/bin/env python

import wx


class DemoPanel1(wx.Panel):
    """
    A very minimal Panel to test Tooltips.
    """
    def __init__(self, *args, **kwargs):
        kwargs['size'] = (200,200)
        wx.Panel.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

    def OnLeftDown(self, event=None):
        print("left clicked")
        self.tooltip = wx.TipWindow(self, text="A tip Window")

        self.tooltip.SetBoundingRect(wx.Rect(event.GetX(), event.GetY(), 20, 20))
        self.tooltip.Show()

    def OnLeave(self, event):
        print("mouse left")
        self.tooltip.Destroy()
        #self.tooltip = None


class DemoPanel2(wx.Panel):
    """
    A very minimal Panel to test Tooltips.
    """
    def __init__(self, *args, **kwargs):
        kwargs['size'] = (200,200)
        wx.Panel.__init__(self, *args, **kwargs)
        self.tooltip = wx.ToolTip(tip='A tool tip') # create an empty tooltip
        #self.tooltip = wx.TipWindow(self, text = "A tip Window")
        #self.tooltip.Hide()
        self.tooltip.SetDelay(100) # set popup delay in ms
        self.SetToolTip(self.tooltip) # connect tooltip to canvas

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeft)
        self.Bind(wx.EVT_MOTION, self.OnMove)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.Rect = (30, 30, 140, 140)

        self.MoveTip = None
        self.count = [0, 0]
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.RED_BRUSH)
        dc.DrawRectangle(*self.Rect)

    def OnLeft(self, event=None):
        print("left clicked")
        self.tooltip = wx.TipWindow(self, text="A tip Window")

    def OnMove(self, event=None):
        if 30 < event.GetX() < 170 and 30 < event.GetY() < 170: # mouse is inside the box
            self.tooltip.Enable(True) # make sure it's enabled
            self.tooltip.SetTip(tip='x=%i\ny=%i' % (event.GetX(), event.GetY()))
            print("enabling the tooltip", self.count[1])
            self.count[1] = self.count[1] + 1
        else: # mouse is outside the axes
            print("outside the box: disabling the tooltip", self.count[0])
            #self.count[0] = self.count[0] + 1
            self.tooltip.Enable(False) # disable the tooltip
            pass


class DemoPanel3(DemoPanel2):
    def OnMove(self, event=None):
        if 30 < event.GetX() < 170 and 30 < event.GetY() < 170: # mouse is inside the box
            self.tooltip.Enable(True) # make sure it's enabled
            self.tooltip.SetTip(tip='x=%i\ny=%i' % (event.GetX(), event.GetY()))
            print("enabling the tooltip", self.count[1])
            self.count[1] = self.count[1] + 1
        else: # mouse is outside the axes
            #print "disabling the tooltip", self.count[0]
            #self.count[0] = self.count[0] + 1
            #self.tooltip.Enable(False) # disable the tooltip
            pass


class DemoFrame(wx.Frame):
    """ This window displays a button """
    def __init__(self, title = "Micro App"):
        wx.Frame.__init__(self, None , -1, title)

        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()

        item = wx.MenuItem(FileMenu, text = "&Quit")
        FileMenu.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnQuit, item)

        MenuBar.Append(FileMenu, "&File")
        self.SetMenuBar(MenuBar)

        P = DemoPanel1(self, pos=(0, 0), style=wx.SUNKEN_BORDER)
        P = DemoPanel2(self, pos=(0, 200), style=wx.SUNKEN_BORDER)

        self.Fit()

    def OnQuit(self,Event):
        self.Destroy()


if __name__ == "__main__":
    app = wx.App(0)
    frame = DemoFrame()
    frame.Show()
    app.MainLoop()
