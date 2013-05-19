#!/usr/bin/env python

import wx
import random
from wxPython.lib import buttons

REFRESH_RATE = 1000 #in ms

class wxBufferedWindow(wx.Window):
    def __init__(self, parent, id,
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.NO_FULL_REPAINT_ON_RESIZE):
        wx.Window.__init__(self, parent, id, pos, size, style | wx.CLIP_CHILDREN)
        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)

    def Draw(self,dc):
        ## just here as a place holder.
        ## This method should be over-ridden when sub-classed
        pass

    def OnPaint(self, event):
        # All that is needed here is to draw the buffer to screen
        dc = wx.BufferedPaintDC(self, self._Buffer)

    def OnSize(self,event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        self.Width, self.Height = self.GetClientSizeTuple()

        # Make new off screen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.EmptyBitmap(self.Width, self.Height)
        self.UpdateDrawing()

    def SaveToFile(self,FileName,FileType):
        """

        This will save the contents of the buffer
        to the specified file. See the wxWindows docs for
        wx.Bitmap::SaveFile for the details

        """
        self._Buffer.SaveFile(FileName,FileType)

    def UpdateDrawing(self):
        """
        This would get called if the drawing needed to change, for whatever reason.

        The idea here is that the drawing is based on some data generated
        elsewhere in the system. If that data changes, the drawing needs to
        be updated.

        """
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.Draw(dc)
        self.Refresh() # This forces a Paint event, so the screen gets updated.
        #self.Update() # If it's not getting updated fast enough, this should force it. 

class DrawWindow(wxBufferedWindow):
    def __init__(self, parent, id = -1):
        ## Any data the Draw() function needs must be initialized before
        ## calling wxBufferedWindow.__init__, as it will call the Draw
        ## function.

        self.DrawData = {}
        wxBufferedWindow.__init__(self, parent, id)
        self.BtnNormal()
        self.BtnBitmap()
        self.CheckB()

    def Draw(self, dc):
        dc.BeginDrawing()
        dc.SetBackground( wx.Brush("Gray") )
        dc.Clear() # make sure you clear the bitmap!

        # Here's the actual drawing code.
        for key,data in self.DrawData.items():
            if key == "Rectangles":
                dc.SetBrush(wx.BLUE_BRUSH)
                dc.SetPen(wx.Pen('VIOLET', 4))
                for r in data:
                    dc.DrawRectangle(*r)
            elif key == "Ellipses":
                dc.SetBrush(wx.Brush("GREEN YELLOW"))
                dc.SetPen(wx.Pen('CADET BLUE', 2))
                for r in data:
                    dc.DrawEllipse(*r)
            elif key == "Polygons":
                dc.SetBrush(wx.Brush("SALMON"))
                dc.SetPen(wx.Pen('VIOLET RED', 4))
                for r in data:
                    dc.DrawPolygon(r)
        dc.EndDrawing()

    def BtnNormal(self):
        self.ID_BUTTON_NORMAL = wx.NewId()
        self.btnNormal = wx.Button(self, self.ID_BUTTON_NORMAL, "normal btn", pos = (100, 100))
        wx.EVT_BUTTON(self, self.ID_BUTTON_NORMAL, self.OnNormalButton)
    def OnNormalButton(self,event=None):
        print "Normal Button Clicked"

    def BtnBitmap(self):
        self.ID_BUTTON_BITMAP = wx.NewId()
        #only bitmap buttons seam to work
        self.buttonTest2 = buttons.wxGenBitmapTextButton(self, self.ID_BUTTON_BITMAP, None, "bitmap btn", pos = (350, 350))
        wx.EVT_BUTTON(self, self.ID_BUTTON_BITMAP, self.OnBitmapButton)
    def OnBitmapButton(self,event=None):
        print "Bitmap Button Clicked"

    def CheckB(self):
        self.ID_SOSO = wx.NewId()
        self.checkB = wx.CheckBox(self, self.ID_SOSO, "test", pos = (50, 50))
        
class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Double Buffered Test",
                         wx.DefaultPosition,
                         size=(500,500),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        ## Set up the MenuBar
        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        ID_EXIT_MENU = wx.NewId()
        file_menu.Append(ID_EXIT_MENU, "E&xit","Terminate the program")
        wx.EVT_MENU(self, ID_EXIT_MENU, self.OnQuit)
        MenuBar.Append(file_menu, "&File")

        draw_menu = wx.Menu()
        ID_DRAW_MENU = wx.NewId()
        draw_menu.Append(ID_DRAW_MENU, "&New Drawing","Update the Drawing Data")
        wx.EVT_MENU(self, ID_DRAW_MENU,self.NewDrawing)
        BMP_ID = wx.NewId()
        draw_menu.Append(BMP_ID,'&Save Drawing\tAlt-I','')
        wx.EVT_MENU(self,BMP_ID, self.SaveToFile)
        MenuBar.Append(draw_menu, "&Draw")
        ID_START = wx.NewId()
        draw_menu.Append(ID_START, "&Start Periodic Update\tF5")
        wx.EVT_MENU(self, ID_START, self.StartUpdate)
        self.SetMenuBar(MenuBar)
        ID_STOP = wx.NewId()
        draw_menu.Append(ID_STOP, "&Stop Periodic Update\tF6")
        wx.EVT_MENU(self, ID_STOP, self.StopUpdate)
        self.SetMenuBar(MenuBar)

        self.Window = DrawWindow(self)
        self.timer = wx.PyTimer(self.Notify)
        #self.timer.Start(REFRESH_RATE)

    def StartUpdate(self, event):
        self.timer.Start(REFRESH_RATE)

    def StopUpdate(self, event):
        self.timer.Stop()

    def Notify(self):
        self.NewDrawing(None)

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
            self.Window.SaveToFile(dlg.GetPath(),wx.BITMAP_TYPE_PNG)
        dlg.Destroy()

    def MakeNewData(self):
        ## This method makes some random data to draw things with.
        MaxX, MaxY = self.Window.GetClientSizeTuple()
        #MaxX = 500
        #MaxY = 500
        DrawData = {}

        # make some random rectangles
        l = []
        for i in range(2):
            w = random.randint(1,MaxX/2)
            h = random.randint(1,MaxY/2)
            x = random.randint(1,MaxX-w)
            y = random.randint(1,MaxY-h)
            l.append( (x,y,w,h) )
        DrawData["Rectangles"] = l

        return DrawData

class DemoApp(wx.App):
    def OnInit(self):
        #wx.InitAllImageHandlers() # called so a PNG can be saved
        frame = TestFrame()
        frame.Show(True)

        ## initialize a drawing
        ## It doesn't seem like this should be here, but the Frame does
        ## not get sized until Show() is called, so it doesn't work if
        ## it is put in the __init__ method.
        frame.NewDrawing(None)

        self.SetTopWindow(frame)

        return True

if __name__ == "__main__":
    app = DemoApp(0)
    app.MainLoop()
