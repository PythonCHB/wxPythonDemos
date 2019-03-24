#!/usr/bin/env python

import wx

print("Using version:", wx.version())

import random

# This has been set up to optionally use the wx.BufferedDC if
# USE_BUFFERED_DC is true, it will be used. Otherwise, it uses the raw
# wx.Memory DC , etc.

USE_BUFFERED_DC = 0


class wxBufferedWindow(wx.ScrolledWindow):

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
                 pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 ## style=wx.NO_FULL_REPAINT_ON_RESIZE
                 ):
        wx.ScrolledWindow.__init__(self, parent, id, pos, size) ##, style)

        self.thumb = 10

        self.Width, self.Height = parent.GetClientSizeTuple()
        self.Width *= 2
        self.Height *= 2

        print("Setting Virtual Size to:", self.Width, self.Height)
        self.SetVirtualSize(wx.Size(self.Width, self.Height))
        self.SetScrollRate(self.thumb, self.thumb)

        # Create a Buffer the vitual size.
        self._Buffer = wx.EmptyBitmap(self.Width, self.Height)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)

    def LeftDown(self, Event):
        print("in LeftDown")
        x, y = Event.GetPosition()
        print("(x,y) is:)", (x, y))
        print("Virtual XY is:", self.CalcUnscrolledPosition(x,y))
        print("Virtual Size of Window is:", self.GetVirtualSize())

    def Draw(self,dc):
        ## just here as a place holder.
        ## This method should be over-ridden when sub-classed
        pass

    def OnPaint(self, event):
        # All that is needed here is to draw the buffer to screen
        if USE_BUFFERED_DC:
            dc = wx.BufferedPaintDC(self, self._Buffer)
        else:
            dc = wx.PaintDC(self)
            self.PrepareDC(dc)
            #print dc
            #print self._Buffer
            dc.DrawBitmap(self._Buffer,0,0)

    def OnSize(self,event):
        print("In OnSize")
        print("Virtual Size is:", self.GetVirtualSize())
        pass
        # perhaps something needs to be done to make sure theuser doesn't make the window bigger than the viftual size.


        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        #self.Width, self.Height = self.GetClientSizeTuple()
        #self.Width *= 2
        #self.Height *= 2
        # maybe re-set Virtual Size here?
        #self.Width, self.Height = self.GetVirtualSize()

        # Make new off screen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        #self._Buffer = wx.EmptyBitmap(self.Width, self.Height)
        #self.UpdateDrawing()

    def SaveToFile(self,FileName,FileType):
        ## This will save the contents of the buffer
        ## to the specified file. See the wx.Windows docs for
        ## wx.Bitmap::SaveFile for the details
        self._Buffer.SaveFile(FileName,FileType)

    def UpdateDrawing(self):
        """
        This would get called if the drawing needed to change, for whatever reason.

        The idea here is that the drawing is based on some data generated
        elsewhere in the system. IF that data changes, the drawing needs to
        be updated.

        """

        if USE_BUFFERED_DC:
            dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
            self.Draw(dc)
        else:
            print("updating the drawing")
            # update the buffer
            dc = wx.MemoryDC()
            dc.SelectObject(self._Buffer)

            self.Draw(dc)
            del dc
            # update the screen
            dc = wx.ClientDC(self)
            self.PrepareDC(dc)
            dc.DrawBitmap(self._Buffer, 0, 0)

            #dc.Blit(0, 0, self.Width, self.Height, dc, 0, 0)

class DrawWindow(wxBufferedWindow):
    def __init__(self, parent, id = -1):
        ## Any data the Draw() function needs must be initialized before
        ## calling wxBufferedWindow.__init__, as it will call the Draw
        ## function.

        self.DrawData = {}
        wxBufferedWindow.__init__(self, parent, id)

    def Draw(self, dc):
        print("In Draw")
        print("DC size is:", dc.GetSize())

        dc.BeginDrawing()
        dc.SetBackground( wx.Brush("White") )
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

        dc.DrawText("(900,900)", 900, 900)
        dc.EndDrawing()


class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Scrolled Double Buffered Test",
                         wx.DefaultPosition,
                         size=(500,500),
                         #style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE
                         )

        ## Set up the MenuBar
        MenuBar = wx.MenuBar()

        file_menu = wx.Menu()
        ID_EXIT_MENU = wx.NewId()
        file_menu.Append(ID_EXIT_MENU, "E&xit", "Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_EXIT_MENU)
        MenuBar.Append(file_menu, "&File")

        draw_menu = wx.Menu()
        ID_DRAW_MENU = wx.NewId()
        draw_menu.Append(ID_DRAW_MENU, "&New Drawing", "Update the Drawing Data")
        self.Bind(wx.EVT_MENU, self.NewDrawing, id=ID_DRAW_MENU)

        BMP_ID = wx.NewId()
        draw_menu.Append(BMP_ID, '&Save Drawing\tAlt-I', '')
        self.Bind(wx.EVT_MENU, self.SaveToFile, id=BMP_ID)
        MenuBar.Append(draw_menu, "&Draw")

        self.SetMenuBar(MenuBar)

        self.Window = DrawWindow(self)

    def OnQuit(self,event):
        self.Close(true)

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
        ## This method makes some random data to draw things with.
        MaxX, MaxY = self.Window.GetVirtualSize()
        #MaxX = 500
        #MaxY = 500
        DrawData = {}

        # make some random rectangles
        l = []
        for i in range(5):
            w = random.randint(1, MaxX / 2)
            h = random.randint(1, MaxY / 2)
            x = random.randint(1, MaxX - w)
            y = random.randint(1, MaxY - h)
            l.append((x, y, w, h))
        DrawData["Rectangles"] = l

        # make some random ellipses
        l = []
        for i in range(5):
            w = random.randint(1, MaxX / 2)
            h = random.randint(1, MaxY / 2)
            x = random.randint(1, MaxX - w)
            y = random.randint(1, MaxY - h)
            l.append((x, y, w, h))
        DrawData["Ellipses"] = l

        # Polygons
        l = []
        for i in range(3):
            points = []
            for j in range(random.randint(3, 8)):
                point = (random.randint(1,MaxX),random.randint(1, MaxY))
                points.append(point)
            l.append(points)
        DrawData["Polygons"] = l

        return DrawData


class DemoApp(wx.App):
    def OnInit(self):
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
