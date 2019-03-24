#!/usr/bin/env python

import wx
import random

# This has been set up to optionally use the wx.BufferedDC if
# USE_BUFFERED_DC is True, it will be used. Otherwise, it uses the raw
# wx.Memory DC , etc.

USE_BUFFERED_DC = 1


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

    def OnPaint(self, event):
        # All that is needed here is to draw the buffer to screen
        if USE_BUFFERED_DC:
            dc = wx.BufferedPaintDC(self, self._Buffer)
        else:
            dc = wx.PaintDC(self)
            dc.DrawBitmap(self._Buffer,0,0)

    def OnSize(self, event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size  = self.GetClientSizeTuple()

        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.EmptyBitmap(Size[0], Size[1])
        self.UpdateDrawing()

    def SaveToFile(self, FileName, FileType):
        ## This will save the contents of the buffer
        ## to the specified file. See the wxWindows docs for
        ## wx.Bitmap::SaveFile for the details
        self._Buffer.SaveFile(FileName,FileType)

    def UpdateDrawing(self):
        """
        This would get called if the drawing needed to change, for whatever reason.

        The idea here is that the drawing is based on some data generated
        elsewhere in the system. IF that data chagnes, the drawing needs to
        be updated.

        """

        if USE_BUFFERED_DC:
            dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
            self.Draw(dc)
        else:
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

        self.DrawData = {}

        ## create a marker bitmap
        print("initing the marker")

        MaskColor = wx.Colour(254, 255, 255)

        self.Marker = wx.EmptyBitmap(40, 40)
        dc = wx.MemoryDC()
        dc.SelectObject(self.Marker)


        dc.BeginDrawing()
        dc.SetBackground(wx.Brush(MaskColor))
        dc.Clear()
        dc.SetPen(wx.RED_PEN)
        dc.SetBrush(wx.GREEN_BRUSH)
        dc.DrawPolygon(((20, 0), (30, 10), (24, 24), (40, 40), (0, 20)))
        dc.EndDrawing()

        ###FIXME### Mask = wx.Mask(self.Marker, MaskColor)
        ###FIXME### self.Marker.SetMask(Mask)

        BufferedWindow.__init__(self, parent, id)


    def Draw(self, dc):
        coords = ((40, 40), (100, 120), (110, 20), (20, 200))
        dc.BeginDrawing()
        dc.SetBackground( wx.Brush("Blue") )
        dc.Clear() # make sure you clear the bitmap!
        try:
            dc.DrawBitmapList(self.Marker, coords, True)
            print("using DrawBitmapList")
        except AttributeError:
            print("not using DrawBitmapList")
            for (x, y) in coords:
                dc.DrawBitmap(self.Marker, x, y, True)
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
        BMP_ID = wx.NewId()
        draw_menu.Append(BMP_ID, '&Save Drawing\tAlt-I','')
        self.Bind(wx.EVT_MENU, self.SaveToFile, id=BMP_ID)
        MenuBar.Append(draw_menu, "&Draw")

        self.SetMenuBar(MenuBar)

        self.Window = DrawWindow(self)


    def OnQuit(self,event):
        self.Close(True)

    def SaveToFile(self,event):
        dlg = wx.FileDialog(self, "Choose a file name to save the image as a PNG to",
                           defaultDir = "",
                           defaultFile = "",
                           wildcard = "*.png",
                           style = wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.Window.SaveToFile(dlg.GetPath(),wx.BITMAP_TYPE_PNG)
        dlg.Destroy()


class DemoApp(wx.App):
    def OnInit(self):
        # wx.InitAllImageHandlers() # called so a PNG can be saved
        frame = TestFrame()
        frame.Show(True)

        ## initialize a drawing
        ## It doesn't seem like this should be here, but the Frame does
        ## not get sized untill Show() is called, so it doesn't work if
        ## it is put in the __init__ method.

        #frame.NewDrawing(None)

        self.SetTopWindow(frame)

        return True


if __name__ == "__main__":
    app = DemoApp(0)
    app.MainLoop()
