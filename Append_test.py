#!/usr/bin/env python

import  wx

BUFFERED = 1

#----------------------------------------------------------------------

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Append_Test",
                         wx.DefaultPosition,
                         size=(800,600),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
       
        self.objects = []        
        self.dragImage = None
        self.DragPaper = None
        self.hiliteObjects = None        
        self.lines = []
        self.maxWidth  = 1000
        self.maxHeight = 1000
        self.x = self.y = 0
        self.curLine = []
        self.drawing = False
        
        self.Paper = wx.Bitmap("Paper.BMP", wx.BITMAP_TYPE_BMP)
        if self.Paper.Ok():
            print "bitmap loaded OK"
        else:
            raise Exception("bitmap DID NOT load OK")

        self.DrawTextOnPaper()
                
#--------------------------------------------------------------------------
        if BUFFERED:
            self.buffer = wx.EmptyBitmap(self.maxWidth, self.maxHeight)
            dc = wx.BufferedDC(None, self.buffer)
            dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
            dc.Clear()
            self.DoDrawing(dc)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        if BUFFERED:
            dc = wx.BufferedPaintDC(self, self.buffer)
        else:
            dc = wx.PaintDC(self)
            self.PrepareDC(dc)
            self.DoDrawing(dc)

    def DrawTextOnPaper(self):

        l1 = ['a','b','c','d']
        text = " "+"".join(l1)

        dc = wx.MemoryDC()
        dc.SelectObject(self.Paper)
        dc.SetFont(wx.Font(36, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Arial"))
        dc.SetTextForeground(wx.BLACK)
        dc.DrawText(text, 155, 25)
        
    def DoDrawing(self, dc, printing=False):
        dc.BeginDrawing()    
        
##        l1 = ['a','b','c','d']
##        text = " "+"".join(l1)
##        bg_colour = wx.Colour(57, 115, 57)  # matches the bg image
##        dc.SetFont(wx.Font(36, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Arial"))
##        dc.SetTextForeground(wx.BLACK)
##        te = dc.GetTextExtent(text)
        
        
        dc.DrawBitmap(self.Paper, 200, 20, True)
        
                
        #dc = wx.MemoryDC()
        #dc.SelectObject(self.manuscript)
        #self.DoDrawing(dc)
        
##        dc.DrawText(text, 225, 25)
        
        dc.EndDrawing()
#--------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        #wx.InitAllImageHandlers
        frame = MyFrame()
        self.SetTopWindow(frame)
        frame.Show(True)

        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

