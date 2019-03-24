#!/usr/bin/env python

"""
A small test of drawing rotated text with a DC

It uses the Buffered Window class from the DoubleBuffer Demo
"""

import wx
import random

from DoubleBufferDemo import BufferedWindow


class DrawWindow(BufferedWindow):
    def __init__(self, parent, id = -1):
        ## Any data the Draw() function needs must be initialized before
        ## calling BufferedWindow.__init__, as it will call the Draw
        ## function.

        self.DrawData = {}
        BufferedWindow.__init__(self, parent, id)

    def Draw(self, dc):
        dc.BeginDrawing()
        dc.SetBackground( wx.Brush("White") )
        dc.Clear() # make sure you clear the bitmap!

        x,y = (250,250)

        str = "  A little Text"

        font = wx.Font(20, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        for angle in range(-180, 180, 45):
            dc.DrawRotatedText(str+" %i"%angle, x, y, angle)

        dc.SetPen(wx.RED_PEN)
        dc.SetBrush(wx.RED_BRUSH)
        dc.DrawCircle(x, y, 4)
        dc.EndDrawing()


class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Double Buffered Test",
                         wx.DefaultPosition,
                         size=(500, 500),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        ## Set up the MenuBar
        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        ID_EXIT_MENU = wx.NewId()
        file_menu.Append(ID_EXIT_MENU, "E&xit","Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_EXIT_MENU)
        MenuBar.Append(file_menu, "&File")

        draw_menu = wx.Menu()
        ID_DRAW_MENU = wx.NewId()
        draw_menu.Append(ID_DRAW_MENU, "&New Drawing","Update the Drawing Data")
        self.Bind(wx.EVT_MENU, self.NewDrawing, id=ID_DRAW_MENU)

        BMP_ID = wx.NewId()
        draw_menu.Append(BMP_ID, '&Save Drawing\tAlt-I', '')
        self.Bind(wx.EVT_MENU, self.SaveToFile, id=BMP_ID)
        MenuBar.Append(draw_menu, "&Draw")

        self.SetMenuBar(MenuBar)

        self.Window = DrawWindow(self)

    def OnQuit(self,event):
        self.Close(True)

    def NewDrawing(self,event):
        self.Window.DrawData = self.MakeNewData()
        self.Window.UpdateDrawing()

    def SaveToFile(self,event):
        dlg = wx.FileDialog(self, "Choose a file name to save the image as a PNG to",
                           defaultDir = "",
                           defaultFile = "",
                           wildcard = "*.png",
                           style = wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.Window.SaveToFile(dlg.GetPath(), wx.BITMAP_TYPE_PNG)
        dlg.Destroy()

    def MakeNewData(self):
        return None


class DemoApp(wx.App):
    def OnInit(self):
        frame = TestFrame()
        frame.Show(True)

        ## initialize a drawing
        ## It doesn't seem like this should be here, but the Frame does
        ## not get sized untill Show() is called, so it doesn't work if
        ## ot is put in the __init__ method.
        frame.NewDrawing(None)

        self.SetTopWindow(frame)

        return True


if __name__ == "__main__":
    print("about to initialize the app")
    app = DemoApp(0)
    app.MainLoop()
