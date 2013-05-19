#!/usr/bin/env python2.4

from wxPython.wx import *


class MyCanvas(wxScrolledWindow):
    def __init__(self, parent, id = -1, size = wxDefaultSize):
        wxScrolledWindow.__init__(self, parent, id , wxPoint(0, 0), size, wxSUNKEN_BORDER)
        ##wxScrolledWindow.__init__(self, parent)
        ## read the image in (this is not a good place to do this in a real app)

        print "about to Init"

        wxInitAllImageHandlers()

        print "done initing"

        #img = wxImage("white_tank.jpg",wxBITMAP_TYPE_JPEG )
        #img = wxImage("white_tank.jpg")
        #bmp = img.ConvertToBitmap()
        #jpg = wxImage(opj('bitmaps/image.jpg'), wxBITMAP_TYPE_JPEG).ConvertToBitmap()

        self.bmp = wxImage('Images/white_tank.jpg', wxBITMAP_TYPE_JPEG ).ConvertToBitmap()

        print "done loading image"

        self.maxWidth, self.maxHeight  = self.bmp.GetWidth(), self.bmp.GetHeight()

        self.SetScrollbars(20, 20, self.maxWidth/20, self.maxHeight/20)

        EVT_PAINT(self, self.OnPaint)

    def OnPaint(self, event):
        dc = wxPaintDC(self)
        self.PrepareDC(dc)
        dc.DrawBitmap(self.bmp, 0, 0)


class TestFrame(wxFrame):
    def __init__(self,parent, id,title,position,size):
        wxFrame.__init__(self,parent, id,title,position, size)


        EVT_CLOSE(self, self.OnCloseWindow)


        self.Canvas1 = MyCanvas(self, wxNewId() )

    def OnCloseWindow(self, event):
        self.Destroy()

class App(wxApp):
    def OnInit(self):
        frame = TestFrame(NULL, -1, "Scroll Test", wxDefaultPosition,(550,200))
        self.SetTopWindow(frame)
        frame.Show(True)
        return true

if __name__ == "__main__":

    app = App(0)
    print "about to start Mainloop"

    app.MainLoop()
     











