#!/usr/bin/env python2.3


import  wx, random


#---------------------------------------------------------------------------

class BufferedScrolledWindow(wx.ScrolledWindow):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

        self.thumb = 10
        
        Width, Height = parent.GetClientSizeTuple()
        self.maxWidth  = Width * 2
        self.maxHeight = Height * 2

#        self.SetBackgroundColour("WHITE")

        self.SetScrollbars(self.thumb, self.thumb, self.maxWidth/self.thumb, self.maxHeight/self.thumb)


        self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def getWidth(self):
        return self.maxWidth

    def getHeight(self):
        return self.maxHeight

    def OnPaint(self, event):
        # Create a buffered paint DC.  It will create the real
        # wx.PaintDC and then blit the bitmap to it when dc is
        # deleted.  Since we don't need to draw anything else
        # here that's all there is to it.
        dc = wx.BufferedPaintDC(self, self.buffer)

    def Draw(self,dc):
        pass

    def UpdateDrawing(self):
        """
        This would get called if the drawing needed to change, for whatever reason.

        The idea here is that the drawing is based on some data generated
        elsewhere in the system. IF that data changes, the drawing needs to
        be updated.

        """

        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.Draw(dc)

    def OnLeftButtonEvent(self, Event):
        print "in LeftDown"
        x, y = Event.GetPosition()
        print "(x,y) is:)", (x, y)
        print "Virtual XY is:", self.CalcUnscrolledPosition(x,y)
        print "Virtual Size of Window is:", self.GetVirtualSize()

    def SetXY(self, event):
        self.x, self.y = self.ConvertEventCoords(event)

    def ConvertEventCoords(self, event):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        return (event.GetX() + (xView * xDelta),
                event.GetY() + (yView * yDelta))



##import wx
##try:
##    print "Using version:", wx.__version__
##except AttributeError:
##    print "Using version:", wx.__revision__

##from wxPython.wx import *

##import random

### This has been set up to optionally use the wxBufferedDC if
### USE_BUFFERED_DC is True, it will be used. Otherwise, it uses the raw
### wxMemory DC , etc.

##USE_BUFFERED_DC = 0

##class wxBufferedWindow(wxScrolledWindow):

##    """

##    A Buffered window class.

##    To use it, subclass it and define a Draw(DC) method that takes a DC
##    to draw to. In that method, put the code needed to draw the picture
##    you want. The window will automatically be double buffered, and the
##    screen will be automatically updated when a Paint event is received.

##    When the drawing needs to change, you app needs to call the
##    UpdateDrawing() method. Since the drawing is stored in a bitmap, you
##    can also save the drawing to file by calling the
##    SaveToFile(self,file_name,file_type) method.

##    """


##    def __init__(self, parent, id,
##                 pos = wxDefaultPosition,
##                 size = wxDefaultSize,
##                 ):
##        wxScrolledWindow.__init__(self, parent, id, pos, size) #, style)

##        self.thumb = 10

##        Width, Height = parent.GetClientSizeTuple()
        
##        noUnitsX = Width * 2 / self.thumb
##        noUnitsY = Height * 2 / self.thumb
        
##        #self.SetScrollRate(self.thumb, self.thumb)
##        #self.SetVirtualSize( (self.thumb * noUnitsX, self.thumb * noUnitsY) )

##        self.SetScrollbars(self.thumb, self.thumb, noUnitsX, noUnitsY )

##        Width, Height = self.GetVirtualSize()

##        # create a Buffer the vitual size
##        print "Virtual Size is:", self.GetVirtualSize()
##        self._Buffer = wxEmptyBitmap(Width/4, Height/4)
    
##        wx.EVT_PAINT(self, self.OnPaint)
##        wx.EVT_SIZE(self, self.OnSize)

##        wx.EVT_LEFT_DOWN(self, self.LeftDown)


##        # OnSize called to make sure the buffer is initialized.
##        # This might result in OnSize getting called twice on some
##        # platforms at initialization, but little harm done.
##        #self.OnSize(None)

##    def LeftDown(self, Event):
##        print "in LeftDown"
##        x, y = Event.GetPosition()
##        print "(x,y) is:)", (x, y)
##        print "Virtual XY is:", self.CalcUnscrolledPosition(x,y)
##        print "Virtual Size of Window is:", self.GetVirtualSize()

##    def Draw(self,dc):
##        ## just here as a place holder.
##        ## This method should be over-ridden when sub-classed
##        pass

##    def OnPaint(self, event):
##        # All that is needed here is to draw the buffer to screen
##        if USE_BUFFERED_DC:
##            dc = wxBufferedPaintDC(self, self._Buffer)
##        else:
##            dc = wxPaintDC(self)
##            self.PrepareDC(dc)
##            #print dc
##            #print self._Buffer
##            dc.DrawBitmap(self._Buffer,0,0)

##    def OnSize(self,event):
##        print "In OnSize"
##        print "Virtual Size is:", self.GetVirtualSize()
##        pass
##        # perhaps something needs to be done to make sure theuser doesn't make the window bigger than the viftual size.
        
        
##        # The Buffer init is done here, to make sure the buffer is always
##        # the same size as the Window
##        #self.Width, self.Height = self.GetClientSizeTuple()
##        #self.Width *= 2
##        #self.Height *= 2
##        # maybe re-set Virtual Size here?
##        #self.Width, self.Height = self.GetVirtualSize()

##        # Make new off screen bitmap: this bitmap will always have the
##        # current drawing in it, so it can be used to save the image to
##        # a file, or whatever.
##        #self._Buffer = wxEmptyBitmap(self.Width, self.Height)
##        #self.UpdateDrawing()

##    def SaveToFile(self,FileName,FileType):
##        ## This will save the contents of the buffer
##        ## to the specified file. See the wxWindows docs for
##        ## wxBitmap::SaveFile for the details
##        self._Buffer.SaveFile(FileName,FileType)

##    def UpdateDrawing(self):
##        """
##        This would get called if the drawing needed to change, for whatever reason.

##        The idea here is that the drawing is based on some data generated
##        elsewhere in the system. IF that data changes, the drawing needs to
##        be updated.

##        """

##        if USE_BUFFERED_DC:
##            dc = wxBufferedDC(wxClientDC(self), self._Buffer)
##            self.Draw(dc)
##        else:
##            print "updating the drawing"
##            # update the buffer
##            dc = wxMemoryDC()
##            dc.SelectObject(self._Buffer)

##            self.Draw(dc)
##            del dc
##            # update the screen
##            dc = wxClientDC(self)
##            self.PrepareDC(dc)
##            dc.DrawBitmap(self._Buffer, 0, 0)
            
##            #dc.Blit(0, 0, self.Width, self.Height, dc, 0, 0)

class DrawWindow(BufferedScrolledWindow):
    def __init__(self, parent, id = -1):
        ## Any data the Draw() function needs must be initialized before
        ## calling wxBufferedWindow.__init__, as it will call the Draw
        ## function.

        self.DrawData = {}
        BufferedScrolledWindow.__init__(self, parent, id)

    def Draw(self, dc):
        print "In Draw"
        print "DC size is:", dc.GetSize()
          
        dc.BeginDrawing()
        dc.SetBackground( wx.Brush("White") )
        dc.Clear() # make sure you clear the bitmap!

        # Here's the actual drawing code.
        for key,data in self.DrawData.items():
            if key == "Rectangles":
                dc.SetBrush(wx.BLUE_BRUSH)
                dc.SetPen(wx.Pen('VIOLET', 4))
                for r in data:
                    dc.DrawRectangleXY(*r)
            elif key == "Ellipses":
                dc.SetBrush(wx.Brush("GREEN YELLOW"))
                dc.SetPen(wx.Pen('CADET BLUE', 2))
                for r in data:
                    dc.DrawEllipseXY(*r)
            elif key == "Polygons":
                dc.SetBrush(wx.Brush("SALMON"))
                dc.SetPen(wx.Pen('VIOLET RED', 4))
                for r in data:
                    dc.DrawPolygon(r)

        dc.DrawText("(900,900)", (900, 900) )
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
            self.Window.SaveToFile(dlg.GetPath(),wx.BITMAP_TYPE_PNG)
        dlg.Destroy()

    def MakeNewData(self):
        ## This method makes some random data to draw things with.
        MaxX, MaxY = self.Window.GetVirtualSize()

        print "in MakeNewData", MaxX, MaxY
        DrawData = {}

        # make some random rectangles
        l = []
        for i in range(5):
            w = random.randint(1,MaxX/2)
            h = random.randint(1,MaxY/2)
            x = random.randint(1,MaxX-w)
            y = random.randint(1,MaxY-h)
            l.append( (x,y,w,h) )
        DrawData["Rectangles"] = l

        # make some random ellipses
        l = []
        for i in range(5):
            w = random.randint(1,MaxX/2)
            h = random.randint(1,MaxY/2)
            x = random.randint(1,MaxX-w)
            y = random.randint(1,MaxY-h)
            l.append( (x,y,w,h) )
        DrawData["Ellipses"] = l

        # Polygons
        l = []
        for i in range(3):
            points = []
            for j in range(random.randint(3,8)):
                point = (random.randint(1,MaxX),random.randint(1,MaxY))
                points.append(point)
            l.append(points)
        DrawData["Polygons"] = l

        return DrawData

class DemoApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers() # called so a PNG can be saved
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















